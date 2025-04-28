from flask import Blueprint
from src.Controllers.AttributesController import atributos

routes = Blueprint("routes", __name__)

routes.route("/atributos", methods=["POST"])(atributos)
