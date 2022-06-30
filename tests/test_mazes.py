import pytest
from api.models import db, User, Maze, UserMazes
from tests.config.invalid_mazes import INVALID_MAZES
from tests.config.valid_mazes_solutions import VALID_MAZES_SOLUTIONS


@pytest.mark.parametrize(('maze', 'message',), INVALID_MAZES)
def test_maze_creation(client, maze, message):
    data = {'username': 'test', 'password': 'test'}
    response = client.post(
        '/user',
        json=data
    )
    login = client.post(
        '/login', json=data
    )
    headers = {"Authorization": f"Bearer {login.json['access_token']}"}

    response = client.post(
        '/maze', json=maze, headers=headers
    )

    assert response.status_code == 422, "Bad response code"
    assert message in response.data, f"Bad response message"


def test_maze_solution_checks(client):
    data = {'username': 'test', 'password': 'test'}
    response = client.post(
        '/user',
        json=data
    )
    login = client.post(
        '/login', json=data
    )
    headers = {"Authorization": f"Bearer {login.json['access_token']}"}

    url = "/maze/{}/solution"
    response = client.get(url.format(100) + "?steps=min", headers=headers)
    assert response.status_code == 404, "Bad response code"

    response = client.get(url.format("sunshine"), headers=headers)
    assert response.status_code == 422, "Bad response code"
    assert b"Invalid maze." in response.data, f"Bad response message"

    # add maze
    response = client.post('/maze', headers=headers, json={
        "entrance": "A1", "gridSize": "8x8",
        "walls": ["C1", "G1", "A2", "C2", "E2", "G2", "C3", "E3", "B4", "C4", "E4", "F4", "G4", "B5", "E5", "B6", "D6",
                  "E6", "G6", "H6", "B7", "D7", "G7", "B8"]
    })
    maze_id = response.json["result"]["id"]
    user = User.query.filter_by(username=data["username"]).first()
    maze = Maze.query.filter_by(id=maze_id).first()
    UserMazes.query.filter_by(user=user.id, maze=maze.id).first()

    response = client.get(url.format(1), headers=headers)
    assert response.status_code == 422, "Bad response code"
    assert b"No steps parameter given." in response.data, f"Bad response message"

    response = client.get(url.format(1) + "?steps=Min", headers=headers)
    assert response.status_code == 422, "Bad response code"
    assert b"Invalid steps value." in response.data, f"Bad response message"


@pytest.mark.parametrize(('maze', 'min_path', 'max_path',), VALID_MAZES_SOLUTIONS)
def test_maze_solution_retrieval(client, maze, min_path, max_path):
    data = {'username': 'test', 'password': 'test'}
    client.post(
        '/user',
        json=data
    )
    login = client.post(
        '/login', json=data
    )
    headers = {"Authorization": f"Bearer {login.json['access_token']}"}

    response = client.post(
        '/maze', json=maze, headers=headers
    )
    maze_id = response.json["result"]["id"]
    response = client.get(
        f'/maze/{maze_id}/solution?steps=min', headers=headers
    )
    assert response.status_code == 200
    assert response.json["path"] == min_path

    response = client.get(
        f'/maze/{maze_id}/solution?steps=max', headers=headers
    )
    assert response.status_code == 200
    assert response.json["path"] == max_path
