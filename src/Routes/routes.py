from flask import Blueprint
from src.Controllers.AttributesController import Atributos
from src.Controllers.ParametrosController import Parametros
from src.Controllers.MediaController import Upload
from src.Controllers.ImagemController import Gerar_csv

routes = Blueprint("routes", __name__)

routes.route("/atributos", methods=["POST"])(Atributos)
routes.route("/parametros", methods=["POST"])(Parametros)
routes.route("/upload", methods=["POST"])(Upload)
routes.route("/gerar-csv", methods=["GET"])(Gerar_csv)
