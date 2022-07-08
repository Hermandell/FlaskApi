from flask import jsonify, request
from bs4 import BeautifulSoup
import json
import requests
from jsonschema import Draft7Validator
from json import load, JSONDecodeError

# abre el archivo schema
with open(r'shema.json') as f:
    schema = load(f)

class MyServer:
    def __init__(self):
        self.LoginUrl = ('https://itnleon.mindbox.app/login/autoriza-alumno')
        self.Profile = ('https://itnleon.mindbox.app/alumnos/datos/generales')
        self.Kardex=('https://itnleon.mindbox.app/alumnos/historico/kardex-calificaciones')
        self.sr = requests
        self.sesion = self.sr.session()
        self.token=None

    def login(self):
        # validar el json que tenga info
        try:
            data = json.loads(request.data)
        except JSONDecodeError:
            return jsonify(({"response": "Error en credenciales"})), 500
        else:
            validar = Draft7Validator(schema)
            errores = list(validar.iter_errors(data))
            #print(errores)
            # aqui va el if not
            ncontrol = data["ncontrol"]
            password = data["password"]
            
            #print(type(data))
            r = requests.get(self.LoginUrl)
            bs = BeautifulSoup(r.text, 'html.parser')
            csrf_token = bs.find('input', attrs={'name': '_token'})['value']
            #print(csrf_token)
            self.token=csrf_token
            credentials = {
                "_token": csrf_token,
                "ncontrol": ncontrol,
                "password": password
            }
            if (not errores):
                if ((len(ncontrol) and len(password)) == 0):
                    return jsonify({"response": "palabra vacia"}),401
                # --------------------------------
                s = self.sesion
#-+---------------------aqui checar porque el api se envia aun cuando da error de credencial----------------
                html=s.post(self.LoginUrl, cookies=r.cookies, data=credentials).text
                #print(html)
                # si no tiene un dropdown menu entonces significa que no se pudo loguear bien
                htmlLog=BeautifulSoup(html, 'html.parser').find('ul', {'class': 'dropdown-menu'})
                if htmlLog is None:
                    return jsonify({"response": "Error de credenciales"}),401
            else:
                return jsonify({"Response": "Error en el response, revise usar strings"}),401
        return jsonify({"token": csrf_token}),200


    def obtenerData(self):
        ##self.login()
        s = self.sesion
        profile = s.get(self.Profile)
        #print(profile.url)
        if profile.status_code == 200:
            if profile.url != self.Profile:
                return ({"response": "Error de Usuario"}),401
            ProfileHtml = BeautifulSoup(profile.text, "html.parser")
            images = ProfileHtml.find('check-img')['image']
            buscar_info = ProfileHtml.find_all('ul', {'class': 'simple'})
            infoGeneral=buscar_info[0]
            li_tagsGeneral = infoGeneral.find_all('li')
            infoGeneralLista=list()
            for i in li_tagsGeneral:
                datos_generales = (i.find('span').text.strip())
                infoGeneralLista.append(datos_generales)
            infoEscolar=buscar_info[1]
            li_tagseEscolar = infoEscolar.find_all('li')
            infoEscolarLista=list()
            for i in li_tagseEscolar:
                datos_Escolares = (i.find('span').text.strip())
                infoEscolarLista.append(datos_Escolares)
            return jsonify([{ 
                "imageprofile": images,
                "id": infoEscolarLista[0],
                #Get first two word of the nombre
                "nombre": infoGeneralLista[0].split()[0].capitalize() + " " + infoGeneralLista[0].split()[1].capitalize(),
                "apellidopaterno": infoGeneralLista[0].split()[2].capitalize(),
                "apellidomaterno": infoGeneralLista[0].split()[3].capitalize(),
                #Se pudiera usar como ID unico tambien la matricula
                "curp": infoGeneralLista[1],
                "fechanacimiento": infoGeneralLista[2],
                "correo": infoGeneralLista[6],
                "sexo": infoGeneralLista[3]
            },{
                "carrera": infoEscolarLista[3],
                "estatus": infoEscolarLista[1],
                "semestre": infoEscolarLista[2],   
            }]),200
        return ({"response": "Falle"}),401
    
    def cali(self):
        #proximanemente...............
        s = self.sesion
        kardex = s.get(self.Kardex)
        if kardex.status_code == 200:
            if kardex.url != self.Kardex:
                return ({"response": "Error de Usuario"}),401
            KardexHtml = BeautifulSoup(kardex.text, "html.parser")
            tablas = KardexHtml.find('ul', {'class': 'simple'})
            #li_tags = ul_tags.find_all('li')
            # print(li_tags)
            info = list()
            for i in li_tags:
                datos_personales = (i.find('span').text.strip())
                info.append(datos_personales)
            print(info)
            return jsonify({
                "imageProfile": images,
                "nombre": info[0],
                "apellidoPaterno": info[1],
                "apellidoMaterno": info[2],
                "curp": info[3],
                "fechaNacimiento": info[4],
                "lugarNacimiento": info[5],
                "sexo": info[6]
            }),200
        return ({"response": "Falle"}),401