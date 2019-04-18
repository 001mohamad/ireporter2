
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()

from flask import request, jsonify, abort

def create_app(config_name):
    from app.api.v1.models.models import Ireporter2

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


    @app.route('/api/vi/Ireporter2/', methods=['POST', 'GET'])
    def ireporter2():
        if request.method == "POST":
            name = str(request.data.get('name', ''))
            if name:
                ireporter = Ireporter2(name=name)
                ireporter.save()
                response = jsonify({
                    'id': ireporter.id,
                    'name': ireporter.name,
                    'email':ireporter.email,
                    'comment': ireporter.comment,
                    'date_created': ireporter.date_created,
                    'date_modified': ireporter.date_modified
                })
                response.status_code = 201
                return response
        else:
            # GET
            ireporter = Ireporter2.get_all()
            results = []

            for ireporter2 in ireporter:
                obj = {
                    'id': ireporter2.id,
                    'name': ireporter2.name,
                    'email':ireporter2.email,
                    'comment': ireporter2.comment,
                    'date_created': ireporter2.date_created,
                    'date_modified': ireporter2.date_modified
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/api/vi/Ireporter2/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def ireporter_manipulation(id, **kwargs):
     # retrieve a ireporter2 using it's ID
        ireporter = Ireporter2.query.filter_by(id=id).first()
        if not ireporter:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        if request.method == 'DELETE':
            ireporter.delete()
            return {
            "message": "ireporter2 {} deleted successfully".format(ireporter.id) 
         }, 200

        elif request.method == 'PUT':
            name = str(request.data.get('name', ''))
            ireporter.name = name
            ireporter.save()
            response = jsonify({
                    'id': ireporter.id,
                    'name': ireporter.name,
                    'email':ireporter.email,
                    'comment': ireporter.comment,
                    'date_created': ireporter.date_created,
                    'date_modified': ireporter.date_modified
            })
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify({
                    'id': ireporter.id,
                    'name': ireporter.name,
                    'email':ireporter.email,
                    'comment': ireporter.comment,
                    'date_created': ireporter.date_created,
                    'date_modified': ireporter.date_modified
            })
            response.status_code = 200
            return response

    return app