from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from functools import wraps
from flasgger import Swagger, swag_from
from config.swagger import template,swagger_config

# clases
from Server import MyServer


# Creating a new Flask application.
app = Flask(__name__)
# Esto es para que los objetos se ordenen
app.config['JSON_SORT_KEYS'] = False
# A configuration for the CORS module.
app.config['CORS_HEADERS'] = 'Content-Type'
# A decorator that allows the server to accept requests from other domains.
CORS(app, supports_credentials=True)
# declarar la clase
myserver = MyServer()
# A decorator that allows the server to accept requests from other domains.

SWAGGER = {
    "title": "Bookmarks API",
    "uiversion": 3,
}

Swagger(app, template=template, config=swagger_config)

def token_required(f):
    """
    If the token is not present in the request header, return a 401 error.

    :param f: The function to be decorated
    :return: a function.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            contar=len(request.headers['Authorization'].split())
            if contar==2:
                token =request.headers['Authorization'].split(' ')[1]
            else:
                token = request.headers['Authorization'].split(' ')[0]
        if token != myserver.token:
            return jsonify({'message': 'Token is missing !!'}), 401
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401
        return f(*args, **kwargs)
    return decorated


# A decorator that allows the server to accept requests from other domains.
@cross_origin(headers=['Content- Type', 'Authorization'])
# A decorator that tells Flask what URL should trigger our function.
@app.route('/login', methods=["POST"])
@swag_from('./docs/Autenticacion/login.yaml')
def login():
    return myserver.login()


@app.route('/user', methods=["GET"])
@swag_from('./docs/dataAlumnos.yaml')
@token_required
def user():
    return myserver.obtenerData()


@app.route('/calificaciones', methods=["GET"])
@token_required
def calificaciones():
    return myserver.cali()

#Obtener la data sin seguridad
@app.route('/all', methods=["POST"])
@swag_from('./docs/todo.yaml')
def todo():
    return myserver.prueba()

if __name__ == '__main__':
    app.run()


# -------------Programacion estrcturada-------------------

# abre el schema
# with open('schema.json') as f:
#     schema = load(f)
#
# app = Flask(__name__)
# # Esto es para que los objetos se ordenen
# app.config['JSON_SORT_KEYS'] = False
# app.config['CORS_HEADERS'] = 'Content-Type'
# CORS(app)
# cors = CORS(app, resources={r"/user": {"origins": "http://localhost:port"}})
#
#
# @app.route('/user', methods=["POST"])
# @cross_origin(origin='127.0.0.1',headers=['Content- Type','Authorization'])
# def user():
#
#     LoginUrl = ('https://itnleon.mindbox.app/login/autoriza-alumno')
#     Profile = ('https://itnleon.mindbox.app/alumnos/datos/generales')
#     #validar el json que tenga info
#     try:
#          data = json.loads(request.data)
#     except JSONDecodeError:
#          return jsonify(({"response": "Error en credenciales"})),500
#     else:
#         validar = Draft7Validator(schema)
#         errores = list(validar.iter_errors(data))
#         print(errores)
#         #aqui va el if not
#         ncontrol = data["ncontrol"]
#         password = data["password"]
#         print(type(data))
#         r = requests.get(LoginUrl)
#         bs = BeautifulSoup(r.text, 'html.parser')
#         csrf_token = bs.find('input', attrs={'name': '_token'})['value']
#         credentials = {
#             "_token": csrf_token,
#             "ncontrol": ncontrol,
#             "password": password
#         }
#         if (not errores):
#             if ((len(ncontrol) and len(password)) == 0):
#                 return jsonify({"response": "palabra vacia"})
#             # --------------------------------
#             s = requests.session()
#             s.post(LoginUrl, cookies=r.cookies, data=credentials)
#             profile = s.get(Profile)
#             print(profile.url)
#             if profile.status_code == 200:
#                 if profile.url != Profile:
#                     return ({"response": "Error de Usuario"})
#                 ProfileHtml = BeautifulSoup(profile.text, "html.parser")
#                 images = ProfileHtml.find('check-img')['image']
#                 ul_tags = ProfileHtml.find('ul', {'class': 'simple'})
#                 li_tags = ul_tags.find_all('li')
#                 # print(li_tags)
#                 info = list()
#                 for i in li_tags:
#                     datos_personales = (i.find('span').text.strip())
#                     info.append(datos_personales)
#
#                 return jsonify({
#                     "imageProfile": images,
#                     "nombre": info[0],
#                     "apellidoPaterno": info[1],
#                     "apellidoMaterno": info[2],
#                     "curp": info[3],
#                     "fechaNacimiento": info[4],
#                     "lugarNacimiento": info[5],
#                     "sexo": info[6]
#                 })
#             return ({"response": "Falle"})
#         else:
#             return jsonify({"Response": "Error en el response, revise usar strings"})
