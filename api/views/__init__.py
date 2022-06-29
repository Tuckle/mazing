from .exceptions import ExceptionHandler
from .users import blueprint as users_blueprint
from .mazes import blueprint as mazes_blueprint


def register_blueprints(app):
    app.register_blueprint(users_blueprint)
    app.register_blueprint(mazes_blueprint)


def register_error_handler(app):
    """ Register function for handling errors  """

    def errorhandler(error):
        response = error.to_json()
        response.status_code = error.status_code
        # print(response.status_code)
        return response

    app.errorhandler(ExceptionHandler)(errorhandler)


funcs = [register_blueprints, register_error_handler]
