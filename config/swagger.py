# A template for the swagger.json file.
template = {
    "swagger": "2.0",
    "info": {
        # This is the information that will be displayed on the Swagger UI.
        "title": "ITNL API",
        "description": "Esta es una API Open Source para impulsar del desarrollo de software en el área de sistemas, brindando la informacion necesaria para aquellos estudiantes quienes quieran utilizar los mismos datos de la institución para hacer mas profesional los proyectos escolares, Utiliza Web Scraping , y JWT",
        "contact": {
            "responsibleOrganization": "",
            "responsibleDeveloper": "",
            "url": "https://github.com/Hermandell",
        },
        # "termsOfService": "www.twitter.com/",
        "version": "1.0"
    },
      # base bash for blueprint registration
    "schemes": [
        # Comento el http porque solo es para modo desarrollo 
        "http",
        "https"
    ],
    
}

swagger_config = {
    # Used to add headers to the swagger.json file.
    "headers": [
    ],
    # Creating a route for the swagger.json file.
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    # The configuration for the Swagger UI.
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
}
