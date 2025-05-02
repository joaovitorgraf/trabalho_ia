from flask import Blueprint
from src.Controllers.AttributesController import Atributos
from src.Controllers.MediaController import Upload, get_urlImage
from src.Controllers.ImagemController import Gerar_csv
from src.Controllers.ProgressoController import obter_progresso
from src.Controllers.RedeNeuralRGBController import Classificar_imagem, Treinar_modelo

from src.Controllers.CNNController import Classificar_imagem_CNN
from src.Controllers.ParametrosCNNController import Definir_parametros_e_treinar
from src.Controllers.UploadControllerCNN import Upload_e_separar

routes = Blueprint("routes", __name__)

routes.route("/atributos", methods=["POST"])(Atributos)
routes.route("/parametros", methods=["POST"])(Treinar_modelo)
routes.route("/upload", methods=["POST"])(Upload)
routes.route("/gerar-csv", methods=["GET"])(Gerar_csv)
routes.route("/progresso", methods=["GET"])(obter_progresso)
routes.route("/get-url-image", methods=["GET"])(get_urlImage)
routes.route("/classificar", methods=["POST"])(Classificar_imagem)

routes.route("/cnn/parametros", methods=["POST"])(Definir_parametros_e_treinar)
routes.route("/cnn/upload", methods=["POST"])(Upload_e_separar)
routes.route("/cnn/classificar", methods=["POST"])(Classificar_imagem_CNN)
