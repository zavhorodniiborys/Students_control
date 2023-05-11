from flask import Flask
from Flask_app.views import controller_views_api

app = Flask(__name__)
app.register_blueprint(controller_views_api)

if __name__ == '__main__':
    app.run(debug=True)
