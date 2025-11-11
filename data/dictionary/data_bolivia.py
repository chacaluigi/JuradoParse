class BoliviaData:
    # OMITED = ["VICENTE", "FRANCO", "JESUS", "ROMAN", "TITO", "PASCUAL"]
    NOMBRES = ["CARMEN","ELENA","NANCY","EVA", "ERICK", "ELIZABETH", "JHILDA", "IRMA", "LEONIDAS", "RIDER", "LIDER","LUZ","JHON","JHONNY","MARY",
        "MARIA", "JOSE", "LUIS", "JUAN", "CARLOS", "ANA", "PEDRO", "MANUEL", "JORGE", "ANTONIO",
        "FRANCISCO", "DAVID", "JAVIER", "MIGUEL", "ALEJANDRO", "RAFAEL", "DANIEL", "SANTIAGO", "ANDRES", "DIEGO",
        "FERNANDO", "RODRIGO", "CRISTIAN", "PABLO", "ALBERTO", "EDUARDO", "ROBERTO", "RICARDO", "GABRIEL", "VICTOR",
        "MARTIN", "OSCAR", "MARCO", "MAURICIO", "WALTER", "SERGIO", "ESTEBAN", "FABIAN", "GERMAN", "RUBEN",
        "ALAN", "ALEX", "ALVARO", "ARMANDO", "ARTURO", "BORIS", "CESAR", "EDGAR", "EDWIN", "ELIAS",
        "EMILIO", "ENRIQUE", "ERNESTO", "FELIPE", "GONZALO", "GUSTAVO", "HECTOR", "HERNAN", "HUGO", "IGNACIO",
        "IVAN", "JOAQUIN", "JULIO", "KEVIN", "LEONARDO", "MARCOS", "MARIO", "MATIAS", "NELSON", "NICOLAS",
        "OMAR", "ORLANDO", "PATRICIO", "RAMIRO", "RENE", "RODOLFO", "ROLANDO", "SAMUEL", "SAUL", "SEBASTIAN",
        "SIMON", "TOMAS", "ULISES", "WILSON", "XAVIER", "AARON", "ABEL", "ADRIAN", "ALDO",
        "AMADO", "AMERICO", "ANGEL", "AUGUSTO", "BENJAMIN", "BERNARDO", "CAMILO", "CARLOS", "CELSO", "CLEMENTE",
        "DAMIAN", "DARIO", "DOMINGO", "EFRAIN", "ELMER", "EMMANUEL", "EVER", "FACUNDO", "FEDERICO", "FELIX",
        "FIDEL", "FLORENTINO", "GILBERTO", "GREGORIO", "GUILLERMO", "HAROLD", "HUMBERTO", "IÑAKI", "ISAIAS",
        "ISIDRO", "ISMAEL", "JACK", "JAIRO", "JAN", "JASON", "JERONIMO", "JOHN", "JONATHAN",
        "JORDI", "JORGE", "JOSUE", "JULIAN", "JULIO", "LAUREANO", "LAZARO", "LEANDRO", "LENIN", "LIONEL",
        "LORENZO", "LUCAS", "LUCIANO", "LUIS", "MARCELO", "MARCIAL", "MARINO", "MARIO", "MARK", "MARTIN",
        "MATEO", "MAX", "MAXIMO", "MICHAEL", "MIGUEL", "MILTON", "MISAEL", "MOISES", "NAHUEL", "NAPOLEON",
        "NESTOR", "NOE", "NOEL", "OCTAVIO", "OLIVER", "OMAR", "OSVALDO", "PABLO", "PASTOR",
        "PATRICIO", "PAUL", "PEDRO", "PLACIDO", "RADAMES", "RAIMUNDO", "RAMIRO", "RAMON", "RANDY", "RAUL",
        "REINALDO", "RENATO", "RENE", "REYNALDO", "RICARDO", "RICHARD", "RIGOBERTO", "ROBINSON", "RODOLFO", "RODOLFO",
        "ROGELIO", "ROMEL", "RONALD", "RONALDO", "RUBEN", "RUFINO", "SALVADOR", "SAMUEL", "SANTIAGO",
        "SAUL", "SEBASTIAN", "SERGIO", "SERVANDO", "SIMON", "STEVEN", "TEODORO", "TIMOTEO", "TOMAS",
        "ULISES", "URIEL", "VALENTIN", "VAN", "VICTOR", "VICTORIO", "VINICIO", "VIRGILIO", "WALTER", "WILLIAM", "WILSON", "XAVIER", "YAMIL", "YURI", "ZACARIAS"
    ]

    NOMBRES_PRUEBA = [
        "ANGULO TEZANOS PINTO FRANKLIN ALBERTO",
        "TEZANOS PINTO MOSTAJO RICARDO ANDRES",
        "ARANCIBIA BETZ LARISSA MARLENE NAT CRIST IS ABD PUNCH",
        "ANTEZANA DIAZ ELVA",
        "ARAOZ DE LA ZERDA SUSANA GABRIELA",
        "ARIAS DE LA CRUZ DENIS PASTOR",
        "ARREAÑO CONDORI JHAMMYLL MICHAEL ESTEBAN",
        "DE LA VIA DE LA ZERDA JORGE LUIS",
        "DE JESUS FARIAS FABIO",
        "DEL CASTILLO DE UGARTE VICTORIA",
        "VEIZAGA DEL VILLAR RICHARD EDMUNDO",
        "MORALES EUGENIA",
        "MORALES DE LA BARRA MAGDALENA",
        "ANTEZANA MARIA DEL CARMEN", 
        "SALAZAR MARIA ANTONIETA",
        "ARANIBAR GUSTAVO ALEX",
        "ARANIBAR JOSE LUIS",
        "VASQUEZ JHILDA NELIDA",
        " VEGA ELIZABETH BETTY",
        "VEGA ERICK ARIEL",
        "LE TONQUEZE GUILLAUME JACQUES PHILIPPE",
        "MERCADO PINELL DEL CASTILLO MAURICIO ALEJANDRO",
        "MENDOZA SAN ROMAN MARIA DE LOS ANGELES MAGALI"
    ]

    APELLIDOS_PRUEBA = [
        "VEGA",
        "ARIAS SANGUEZA",
        "ARELLANO ORTUSTE",
        "ANGULO TEZANOS PINTO",
        "MERCADO PINELL DEL CASTILLO",
        "MENDOZA SAN ROMAN",
        "TEZANOS PINTO MOSTAJO",
        "DE LA VIA DE LA ZERDA",
        "DE LA MANUEL TEZANOS PINTO"
    ]

    DOCUMENTOS_PRUEBA = [
        "I-3623322","P-6445020","M-51258-88","R-4007-030171C","R-4000-200160D","I-14187764","M-179514384"
    ]

class PDFConfig:
    # Diccionario con configuraciones de PDFs
    CONFIGURACIONES = {
        
        '2019_EG_CBBA': {
            'type': 'normal',
            'pdf_path': './data/raw/2019-10-20-Elecciones-Generales-Cochabamba.pdf',
            'flavor': 'lattice',
            'first_page': '1',
            'first_top_cut': None,
            'all_pages': '1-505',
            'all_top_cut': None,
            'column_separators': None,
            'column_names': [
                'NRO',
                'APELLIDOS Y NOMBRES',
                'DOCUMENTO',
                'MUNICIPIO',
                'RECINTO',
                'MESA'
            ]
        },
        
        '2020_EG_CBBA': {
            'type': 'areas',
            'pdf_path': './data/raw/2020-10-18-Elecciones-Generales-Cochabamba.pdf',
            'flavor': 'stream',
            'first_page': '4',
            'first_top_cut': '0.178',
            'all_pages': '5-97',
            'all_top_cut': None,
            'column_separators': [
                ['78.10,113.30,154.7,244.17'],
                ['338.5,366.7,415.67,492.93'],
                ['587.14,615.14,663.92,740.95']
            ],
            'column_names': [
                'APELLIDOS Y NOMBRES',
                'DOCUMENTO',
                'MUNICIPIO',
                'RECINTO',
                'MESA'
            ]
        },

        '2021_ES_CBBA': {
            'type': 'areas',
            'pdf_path': './data/raw/2021-03-07-Elecciones-Subnacionales-Cochabamba.pdf',
            'flavor': 'stream',
            'first_page': '4',
            'first_top_cut': '0.178',
            'all_pages': '5-99',
            'all_top_cut': '0.968',
            'column_separators': [
                ['88.10,117.30,165.70,242.95'],
                ['337.5,365.7,414.67,491.90'],
                ['585.90,614.3,662.92,738.95']
            ],
            'column_names': [
                'APELLIDOS Y NOMBRES',
                'DOCUMENTO',
                'MUNICIPIO',
                'RECINTO',
                'MESA'
            ]
        },

        '2024_EJ_CBBA': {
            'type': 'normal',
            'pdf_path': './data/raw/2024-12-15-Elecciones-Judiciales-Cochabamba.pdf',
            'flavor': 'lattice',
            'first_page': '16',
            'first_top_cut': None,
            'all_pages': '16-337',
            'all_top_cut': None,
            'column_separators': None,
            'column_names': [
                'NRO',
                'APELLIDOS',
                'NOMBRES',
                'TIPO',
                'DOCUMENTO',
                'COMP',
                'MUNICIPIO',
                'RECINTO',
                'MESA'
            ]
        },
    }
    
    @classmethod
    def get_config(cls, pdf_key):
        return cls.CONFIGURACIONES.get(pdf_key)
    
    @classmethod
    def get_attributes(cls, pdf_key, *attributes):
        config = cls.get_config(pdf_key)
        if config:
            return tuple(config.get(attr) for attr in attributes)
        return tuple(None for _ in attributes)
    
    @classmethod
    def get_config(cls, pdf_key):
        return cls.CONFIGURACIONES.get(pdf_key, {})

