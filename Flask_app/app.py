from flask import Flask
from controller_api_endpoints import controller_blueprint

app = Flask(__name__)
app.register_blueprint(controller_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
