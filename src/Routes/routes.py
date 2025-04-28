from flask import Blueprint
from src.Controllers.AttributesController import Atributos
from src.Controllers.ParametrosController import Parametros

routes = Blueprint("routes", __name__)

routes.route("/atributos", methods=["POST"])(Atributos)
routes.route("/parametros", methods=["POST"])(Parametros)
