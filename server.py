from flask_app import app
from flask_app.controllers import users, athletes, injuries


if __name__ == '__main__':
    app.run(debug=True, port=5005)