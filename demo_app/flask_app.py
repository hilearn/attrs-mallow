from flask import Flask
from flask_smorest import Api, Blueprint
from flask_restful import Resource

from marshmallow_helpers import EnumField
from .enum_schema import EnumQuery, EnumResponse, AllowNoneDict, ByKey, Derived

bp = Blueprint('EnumField demo', __name__)


@bp.route('/enum_demo')
class EnumDemo(Resource):
    @bp.arguments(EnumQuery.schema, location='json', required=True,
                  example={'int_enum': 1, 'str_enum': 'second'},
                  as_kwargs=True)
    @bp.response(EnumResponse.schema)
    def post(self, int_enum, str_enum):
        return {'int_enum': int_enum, 'str_enum': str_enum}, 200

    def get(self):
        return {}


@bp.route('/none_obj_demo')
class NoneObjDemo(Resource):
    @bp.arguments(AllowNoneDict.schema, location="json",
                  required=True, as_kwargs=True)
    @bp.response(AllowNoneDict.schema)
    def post(self, obj, integer):
        return {"obj": obj, "integer": integer}


@bp.route('/by_key')
class ByKeyDemo(Resource):
    @bp.arguments(ByKey.schema, location="json", required=True, as_kwargs=True)
    @bp.response(ByKey.schema)
    def post(self, key):
        return {"key": key}


@bp.route('/derived')
class DerivedDemo(Resource):
    @bp.arguments(Derived.schema, location="json",
                  required=True, as_kwargs=True)
    @bp.response(Derived.schema)
    def post(self, string, integer):
        return {"integer": integer + 1, "string": string}


app = Flask(__name__)

app.config['OPENAPI_VERSION'] = '3.0.2'
app.config['OPENAPI_URL_PREFIX'] = 'spec'

app.config['OPENAPI_SWAGGER_UI_PATH'] = 'swagger'
app.config['OPENAPI_SWAGGER_UI_VERSION'] = '3.19.5'

app.config['OPENAPI_REDOC_PATH'] = 'redoc'
app.config['OPENAPI_REDOC_VERSION'] = 'next'

api = Api(app)
api.register_field(EnumField, 'string', None)

api.register_blueprint(bp)
