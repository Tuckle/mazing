import traceback

import sqlalchemy.exc
from flask import Blueprint, request, Response, jsonify
from api.models import Maze, UserMazes, db, User
from api.core import create_response, serialize_list
from flask_cors import CORS, cross_origin
from flask_jwt_extended import jwt_required, get_jwt
from api.lib.maze import InvalidMazeException, solve_maze

blueprint = Blueprint("mazes", __name__)


@blueprint.route('/maze', methods=("POST", "GET"))
@cross_origin(supports_credentials=True)
@jwt_required()
def create_or_get_maze():
    info = get_jwt()
    user = int(info["sub"])
    defaults = dict()

    if request.method == "POST":
        data = request.get_json()
        try:
            for key in ["entrance", "gridSize", "walls"]:
                assert key in data and data[key], f"No {key} provided"
                defaults[key] = data[key]
            assert "A" <= data["entrance"][0] <= "Z", "Invalid entrance row character"
            try:
                int(data["entrance"][1:])
            except ValueError:
                raise AssertionError("Invalid entrance column number")

            grid = data["gridSize"]
            assert "x" in grid, "Invalid gridSize format"
            try:
                list(map(int, grid.split('x')))
            except ValueError:
                raise AssertionError("Invalid gridSize")
        except AssertionError as aer:
            return create_response(status=422, message=str(aer))

        try:
            min_path, max_path = solve_maze(data["entrance"], grid, data["walls"])
        except InvalidMazeException as err:
            return create_response(status=422, message=str(err))
        defaults["walls"] = ",".join(defaults["walls"])
        defaults["grid"] = defaults.pop("gridSize")
        defaults_primary = defaults.copy()
        defaults["min_path"] = ",".join(min_path) if min_path else None
        defaults["max_path"] = ",".join(max_path) if max_path else None

        maze, created = Maze.get_or_create(Maze, defaults, **defaults_primary)
        user_maze = UserMazes(user_id=user, maze_id=maze.id)
        try:
            db.session.add(user_maze)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return create_response(message="Entry already exists.")
        return create_response(message="Maze successfully added.")

    elif request.method == "GET":
        # return all mazes id for current user
        mazes = db.session.query(Maze.id).filter(
            User.id == user
        ).filter(UserMazes.user == User.id).filter(UserMazes.maze == Maze.id).all()
        return jsonify({
            "mazes": list(map(lambda x: x[0], mazes))
        })
    else:
        return create_response(status=405, message="Method not allowed")


@blueprint.route('/maze/<maze>/solution', methods=("GET",))
@cross_origin(supports_credentials=True)
@jwt_required()
def get_maze_solution(maze):
    steps = request.args.get('steps')
    info = get_jwt()
    user = int(info["sub"])

    try:
        assert steps, "No steps parameter given"
        assert steps in {"min", "max"}, "Invalid steps value"
    except AssertionError as aer:
        return create_response(status=422, message=str(aer))

    try:
        maze = db.session.query(Maze).filter(
            UserMazes.user == user
        ).filter(UserMazes.maze == maze).filter(Maze.id == maze).all()[0]
        assert maze
    except (sqlalchemy.exc.NoResultFound, IndexError, AssertionError) as aer:
        return create_response(status=404)

    if steps == "min":
        result = maze.min_path
    else:
        result = maze.max_path
        if not result:
            result = maze.min_path
    result = result.split(',')
    return jsonify({
        "path": result
    })
