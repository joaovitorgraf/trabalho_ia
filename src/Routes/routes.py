from flask import Blueprint
from src.Controllers.AttributesController import Atributos
from src.Controllers.MediaController import Upload, get_urlImage
from src.Controllers.ImagemController import Gerar_csv
from src.Controllers.ProgressoController import obter_progresso
from src.Controllers.RedeNeuralRGBController import Classificar_imagem, Treinar_modelo

routes = Blueprint("routes", __name__)

routes.route("/atributos", methods=["POST"])(Atributos)
routes.route("/parametros", methods=["POST"])(Treinar_modelo)
routes.route("/upload", methods=["POST"])(Upload)
routes.route("/gerar-csv", methods=["GET"])(Gerar_csv)
routes.route("/progresso", methods=["GET"])(obter_progresso)
routes.route("/get-url-image", methods=["GET"])(get_urlImage)
routes.route("/classificar", methods=["POST"])(Classificar_imagem)
