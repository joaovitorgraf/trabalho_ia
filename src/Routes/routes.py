from flask import Blueprint
from src.Controllers.AttributesController import attributes

routes = Blueprint("routes", __name__)

routes.route("/attributes", methods=["POST"])(attributes)
