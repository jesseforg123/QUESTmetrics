from app import app, api
from resources.register_resources import registerResources
import os
import flask

registerResources(api)

if __name__ == '__main__':
    app.run(host="0.0.0.0")