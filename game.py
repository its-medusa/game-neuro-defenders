import json
import random
import time
import os
import base64
from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
from pywebio.session import run_js

# --- 1. CONFIGURACIÓN IMAGENES Y AUDIO ---
ARCHIVO_AUDIO = 'images/C418-Blind-Spots-Minecraft.mp3'
ARCHIVO_PDF = 'info.pdf' 

def cargar_imagen(path):
    try:
        return open(path, 'rb').read()
    except FileNotFoundError:
        return None

IMAGENES = {
    'portada': cargar_imagen('images/portada_neoquito.png'),
    'registro': cargar_imagen('images/registro_fondo.png'),
    'base': cargar_imagen('images/fondo_misiones.png'),
    'fiesta': cargar_imagen('images/fondo_fiesta.png'),
    'bano': cargar_imagen('images/fondo_bano.png'),
    'mercado': cargar_imagen('images/fondo_mercado.png'),
    'callejon': cargar_imagen('images/fondo_callejon.png'),
    'parque': cargar_imagen('images/fondo_parque.png'),
    'laboratorio': cargar_imagen('images/fondo_laboratorio.png'),
    'vip': cargar_imagen('images/fondo_vip.png'),
    'botiquin': cargar_imagen('images/fondo_botiquin.png'),
    'enemigo_fiesta': cargar_imagen('images/enemigo_fiesta.png'),
    'enemigo_vape': cargar_imagen('images/enemigo_vape.png'),
    'enemigo_adulterado': cargar_imagen('images/enemigo_adulterado.png'),
    'enemigo_coca': cargar_imagen('images/enemigo_coca.png'),
    'enemigo_marihuana': cargar_imagen('images/enemigo_marihuana.png'),
    'enemigo_fentanilo': cargar_imagen('images/enemigo_fentanilo.png'),
    'enemigo_tusi': cargar_imagen('images/enemigo_tusi.png'),
    'enemigo_farmacos': cargar_imagen('images/enemigo_farmacos.png'),
    'trofeo': cargar_imagen('images/trofeo.png'),
    'game_over': cargar_imagen('images/game_over.png'),
    'jefe': cargar_imagen('images/jefe.png'),
    'fondo_jefe': cargar_imagen('images/fondo_jefe.png')
}

# --- 2. BASE DE DATOS DE PREGUNTAS ---
DB_PREGUNTAS = {
    'fiesta': [ # Alcohol
        {"p": "¿Cuál es el órgano que más sufre con el alcohol?", "correcta": "Hígado.", "falsas": ["Riñones.", "Estómago.", "Pulmones."], "info": "INFO: El hígado descompone el alcohol. El exceso causa cirrosis irreversible."},
        {"p": "Mito: 'Beber café o ducharse baja la borrachera'.", "correcta": "Mito.", "falsas": ["Realidad."], "info": "INFO: Solo el tiempo elimina el alcohol. El café solo te despierta, pero sigues ebrio."},
        {"p": "¿Qué es el 'Binge Drinking'?", "correcta": "Beber mucho en poco tiempo.", "falsas": ["Beber una copa al día.", "Beber solo cerveza."], "info": "INFO: Aumenta drásticamente el riesgo de coma etílico y daño cerebral."},
        {"p": "El alcohol es un depresor. ¿Qué significa?", "correcta": "Ralentiza el cerebro.", "falsas": ["Te pone triste siempre.", "Acelera el corazón."], "info": "INFO: Afecta la coordinación, el habla y el juicio."},
        {"p": "¿Efecto en adolescentes vs adultos?", "correcta": "Daña más el cerebro joven.", "falsas": ["El mismo efecto.", "Afecta menos."], "info": "INFO: El cerebro termina de formarse a los 25 años. El alcohol daña la memoria permanentemente."}
    ],
    'vape': [ # Vape
        {"p": "¿Qué sustancia adictiva tienen la mayoría de vapes?", "correcta": "Nicotina.", "falsas": ["Cafeína.", "Taurina."], "info": "INFO: La nicotina es altamente adictiva y altera el desarrollo cerebral."},
        {"p": "¿Qué es el 'Pulmón de Palomitas'?", "correcta": "Enfermedad grave por saborizantes.", "falsas": ["Una marca de vape.", "Sensación agradable."], "info": "INFO: El diacetilo causa cicatrización permanente en los pulmones (bronquiolitis)."},
        {"p": "Vape: 'El vapor del vape es solo agua'.", "correcta": "Mito.", "falsas": ["Realidad."], "info": "INFO: Es un aerosol con partículas finas, metales pesados y químicos cancerígenos."},
        {"p": "¿Vapear lleva a fumar cigarrillos?", "correcta": "Sí, aumenta probabilidades.", "falsas": ["No, lo evita.", "No hay relación."], "info": "INFO: Se conoce como 'puerta de entrada'. La adicción a la nicotina facilita el paso al tabaco."},
        {"p": "¿Qué pasa si explota la batería?", "correcta": "Quemaduras severas.", "falsas": ["Nada grave.", "Solo se daña el equipo."], "info": "INFO: Las baterías de litio defectuosas han causado lesiones graves en cara y manos."}
    ],
    'coca': [ # Cocaína
        {"p": "Cocaína: Riesgo cardíaco inmediato:", "correcta": "Infarto o paro cardíaco.", "falsas": ["El corazón late lento.", "Mejora circulación."], "info": "INFO: La cocaína eleva la presión y contrae los vasos sanguíneos peligrosamente."},
        {"p": "Efecto del 'bajón' (cuando pasa el efecto):", "correcta": "Paranoia y depresión severa.", "falsas": ["Alegría extrema.", "Sueño profundo."], "info": "INFO: Al agotarse la dopamina, el cerebro cae en un estado depresivo que incita a consumir más."},
        {"p": "¿Qué le pasa al tabique nasal?", "correcta": "Se perfora o destruye.", "falsas": ["Se fortalece.", "Crece más."], "info": "INFO: La falta de riego sanguíneo mata el tejido (necrosis)."},
        {"p": "Cocaína + Alcohol produce:", "correcta": "Cocaetileno (Muy tóxico).", "falsas": ["Etanol puro.", "Adrenalina."], "info": "INFO: El cocaetileno es mucho más tóxico para el hígado y corazón que ambas drogas por separado."},
        {"p": "'La cocaína no causa adicción física'.", "correcta": "Mito.", "falsas": ["Realidad."], "info": "INFO: Causa cambios físicos en el cerebro creando una dependencia muy fuerte."}
    ],
    'adulterado': [ # Alcohol Adulterado
        {"p": "¿Qué químico mortal se usa para adulterar?", "correcta": "Metanol.", "falsas": ["Etanol.", "Glucosa."], "info": "INFO: El metanol es alcohol industrial. El cuerpo lo convierte en veneno puro."},
        {"p": "Síntoma clave de intoxicación:", "correcta": "Visión borrosa o ceguera.", "falsas": ["Mucha hambre.", "Hiperactividad."], "info": "INFO: El metanol ataca directamente el nervio óptico. Ve a urgencias de inmediato."},
        {"p": "¿Cómo sospechar de una botella?", "correcta": "Etiqueta mala / Precio bajo.", "falsas": ["Si la botella es bonita.", "Si sabe dulce."], "info": "INFO: Desconfía de licores excesivamente baratos o con etiquetas mal pegadas."},
        {"p": "Si sospechas que bebiste adulterado:", "correcta": "Ir al hospital inmediatamente.", "falsas": ["Dormir.", "Beber agua con azúcar."], "info": "INFO: El tiempo es vida. El tratamiento temprano evita la ceguera o muerte."},
        {"p": "Alcohol adulterado: 'Si huele a alcohol, es seguro'.", "correcta": "Mito.", "falsas": ["Realidad."], "info": "INFO: El metanol huele y sabe muy parecido al etanol. No puedes diferenciarlo probando."}
    ],
    'marihuana': [ # El Parque
        {"p": "¿Compuesto psicoactivo principal?", "correcta": "THC.", "falsas": ["CBD.", "ABC."], "info": "INFO: El THC es el responsable de la alteración mental."},
        {"p": "Marihuana: 'No afecta la memoria'.", "correcta": "Mito.", "falsas": ["Realidad."], "info": "INFO: El consumo reduce la capacidad de aprender, memorizar y resolver problemas."},
        {"p": "¿La marihuana puede causar problemas psiquiátricos?", "correcta": "Sí, puede detonar esquizofrenia.", "falsas": ["No, relaja la mente.", "Solo si se mezcla."], "info": "INFO: En jóvenes predispuestos puede despertar enfermedades mentales permanentes."},
        {"p": "¿Fumar marihuana afecta los pulmones?", "correcta": "Sí, igual o más que el tabaco.", "falsas": ["No, es natural.", "Limpia los pulmones."], "info": "INFO: El humo contiene muchas de las mismas toxinas cancerígenas que el tabaco."},
        {"p": "¿Qué es el síndrome amotivacional?", "correcta": "Apatía y pereza crónica.", "falsas": ["Estar muy feliz.", "Tener hambre."], "info": "INFO: Pérdida de ambición e interés en metas personales o estudios."}
    ],
    'fentanilo': [ # El Laboratorio
        {"p": "¿Qué es el fentanilo?", "correcta": "Opioide sintético mortal.", "falsas": ["Estimulante suave.", "Una hierba."], "info": "INFO: Es 50 veces más fuerte que la heroína. Una dosis minúscula es mortal."},
        {"p": "¿Por qué es tan peligroso el fentanilo en el mercado?", "correcta": "Lo mezclan sin avisar.", "falsas": ["Es muy caro.", "Tiene mal sabor."], "info": "INFO: Traficantes lo añaden a otras drogas para abaratar. Muchos no saben que lo consumen."},
        {"p": "¿Qué cantidad se considera letal?", "correcta": "2mg (granos de sal).", "falsas": ["Una cucharada.", "Un gramo."], "info": "INFO: Solo 2 miligramos pueden detener tu respiración."},
        {"p": "¿Medicamento para revertir sobredosis?", "correcta": "Naloxona (Narcan).", "falsas": ["Aspirina.", "Insulina."], "info": "INFO: Bloquea los efectos de los opioides y puede restablecer la respiración."},
        {"p": "¿Causa de muerte por fentanilo?", "correcta": "Detiene la respiración.", "falsas": ["Explota el corazón.", "Sube la temperatura."], "info": "INFO: Deprime el sistema respiratorio hasta que el usuario deja de respirar."}
    ],
    'tusi': [ # El VIP
        {"p": "¿Qué contiene el 'Tusi' (polvo rosa)?", "correcta": "Mezcla (Ketamina + MDMA).", "falsas": ["Cocaína pura.", "Fresas trituradas."], "info": "INFO: Rara vez tiene cocaína. Es un cóctel químico impredecible."},
        {"p": "¿Por qué es peligrosa la mezcla de diferentes drogas?", "correcta": "Efectos contrarios (Sube/Baja).", "falsas": ["Mancha la ropa.", "Es muy dulce."], "info": "INFO: Confunde al sistema nervioso y aumenta riesgo de arritmias."},
        {"p": "¿Qué es la Ketamina (base)?", "correcta": "Anestésico disociativo.", "falsas": ["Vitamina.", "Azúcar."], "info": "INFO: Provoca sensación de separación del cuerpo y la realidad."},
        {"p": "Drogas: 'El Tusi es droga segura de élite'.", "correcta": "Mito.", "falsas": ["Realidad."], "info": "INFO: Es puro marketing. Al ser mezcla casera, nunca sabes qué consumes."},
        {"p": "¿Riesgo social asociado?", "correcta": "Vulnerabilidad y abuso.", "falsas": ["Mejorar relaciones.", "Ser más inteligente."], "info": "INFO: La desconexión y sedación deja al usuario vulnerable a agresiones."}
    ],
    'farmacos': [ # El Botiquín
        {"p": "Peligro de benzodiacepinas (tranquilizantes):", "correcta": "Alta dependencia.", "falsas": ["Ninguno si es medicina.", "Superpoderes."], "info": "INFO: Generan adicción rápido. Dejarlas de golpe puede ser peligroso."},
        {"p": "Mezcla Tranquilizantes + Alcohol:", "correcta": "Potenciación letal.", "falsas": ["Se anulan.", "Te diviertes más."], "info": "INFO: Ambos bajan el ritmo del cuerpo. Juntos pueden parar tu respiración."},
        {"p": "Abuso de jarabes con codeína:", "correcta": "Opioide muy adictivo.", "falsas": ["Es inofensivo.", "Cura más rápido."], "info": "INFO: Es familia de la morfina. Causa adicción fuerte y riesgo de sobredosis."},
        {"p": "Fármacos: 'Si lo vende la farmacia, no es droga'.", "correcta": "Mito.", "falsas": ["Realidad."], "info": "INFO: El abuso de fármacos sin control médico mata a miles cada año."},
        {"p": "Abuso de estimulantes (TDAH):", "correcta": "Ansiedad y problemas cardíacos.", "falsas": ["Mejora notas sin riesgo.", "Da sueño."], "info": "INFO: Forzar el cerebro provoca desgaste severo e insomnio."}
    ]
}

# --- 3. ESTADO DEL JUGADOR ---
jugador = {"nombre": "Invitado", "xp": 0, "vida": 100, "misiones": []}

# --- 4. SISTEMA VISUAL Y AUDIO ---

def inyectar_estilo_transparente():
    """
    CSS: Hace todo transparente para que se vea el fondo.
    """
    put_html("""
    <style>
        /* 1. Hace transparente a PyWebIO para ver la imagen de fondo */
        body, html, #pywebio-scope-root, .container, .main, .footer, div, .row, .col {
            background: transparent !important;
            background-color: transparent !important;
            box-shadow: none !important;
        }
        
        /* 2. Fondo de seguridad (solo se ve si falla la imagen) */
        body { background-color: black !important; font-family: 'Verdana', sans-serif; }

        /* 3. Estilo de las Tarjetas */
        .card, .modal-content { 
            background-color: rgba(0, 0, 0, 0.95) !important; 
            border: 2px solid #00ff00 !important;
            color: white !important;
            box-shadow: 0 0 20px #00ff00;
            border-radius: 15px;
        }
        
        /* 4. Inputs */
        input[type="text"], select, textarea, .form-control {
            background-color: #002200 !important;
            color: white !important;
            border: 1px solid #00ff00 !important;
            font-size: 18px !important;
        }
        
        /* 5. Botones */
        .btn-primary { 
            background-color: #00ff00 !important; 
            color: black !important; 
            font-weight: bold; 
            border: none;
            text-transform: uppercase;
            box-shadow: 0 0 10px #00ff00; 
        }
        .btn-danger { 
            background-color: red !important; 
            color: white !important; 
            border: none;
            box-shadow: 0 0 10px red;
        }
        
        /* 6. Textos */
        label { color: #00ff00 !important; font-weight: bold; font-size: 16px; }
        .close { color: white !important; opacity: 1; }
        
        /* 7. Eliminar barra de scroll si no es necesaria */
        body { overflow-x: hidden; }
    </style>
    """)

def mostrar_enemigo(clave_imagen, nombre, color):
    """
    Función visual para mostrar al enemigo centrado.
    """
    # Usamos un contenedor flexible para centrar todo
    with put_column().style('display: flex; flex-direction: column; align-items: center; margin: 20px 0;'):
        # La Imagen con borde brillante
        put_image(IMAGENES[clave_imagen], width='250px').style(f'''
            background: white; 
            border: 4px solid white; 
            border-radius: 15px; 
            box-shadow: 0 0 30px {color};
        ''')
        # El Nombre con fondo negro
        put_text(nombre).style(f'''
            background: black; 
            color: {color}; 
            padding: 8px 20px; 
            border: 2px solid {color}; 
            border-radius: 8px; 
            margin-top: 15px; 
            font-family: monospace; 
            font-weight: bold; 
            font-size: 18px;
            text-transform: uppercase;
            box-shadow: 0 0 10px {color};
        ''')

def sistema_audio():
    """
    Sistema de audio seguro. Usa HTML puro y {{ }} para evitar errores de Python.
    """
    try:
        with open(ARCHIVO_AUDIO, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            src = f"data:audio/mp3;base64,{b64}"
            
            # El código JS está protegido con dobles llaves {{ }}
            audio_html = f"""
            <div style="position: fixed; top: 10px; right: 10px; z-index: 9999;">
                <audio id="musica" loop autoplay>
                    <source src="{src}" type="audio/mp3">
                </audio>
                <button onclick="var a=document.getElementById('musica'); if(a.paused) a.play(); else a.pause();" 
                        style="background:black; color:#0f0; border:2px solid #0f0; border-radius:50%; width:40px; height:40px; font-size:20px; cursor:pointer;">
                    🔊
                </button>
                <script>
                    var a = document.getElementById("musica");
                    a.volume = 0.3;
                    document.addEventListener('click', function() {{ a.play(); }}, {{once:true}});
                </script>
            </div>
            """
            
            run_js(f"""
            if(!document.getElementById('musica')) {{
                var d = document.createElement('div');
                d.innerHTML = `{audio_html}`;
                document.body.appendChild(d);
            }}
            """)
    except:
        pass

# --- 5. RANKING ---

def inyectar_estilos_nucleares():
    """
    CSS: Hace todo transparente para que se vea el fondo.
    """
    put_html("""
    <style>
        /* 1. Transparencia total para PyWebIO */
        body, html, #pywebio-scope-root, .container, .main, .footer, div, .row, .col {
            background: transparent !important;
            background-color: transparent !important;
            box-shadow: none !important;
        }
        
        /* 2. Fondo de seguridad negro */
        body { background-color: black !important; font-family: 'Verdana', sans-serif; }

        /* 3. Estilo NEÓN para las tarjetas */
        .card, .modal-content { 
            background-color: rgba(0, 0, 0, 0.95) !important; 
            border: 2px solid #00ff00 !important;
            color: white !important;
            box-shadow: 0 0 20px #00ff00;
            border-radius: 15px;
            margin-top: 5vh !important;
            max-width: 600px !important;  /* 600px es ideal: ni muy ancho ni muy angosto */
            margin-left: auto !important; /* Centrado */
            margin-right: auto !important;/* Centrado */
        }
        
        /* 4. Inputs y Textos */
        input[type="text"], select, textarea, .form-control {
            background-color: #002200 !important;
            color: white !important;
            border: 1px solid #00ff00 !important;
            font-size: 18px !important;
        }
        
        /* 5. Botones */
        .btn-primary { 
            background-color: #00ff00 !important; 
            color: black !important; 
            font-weight: bold; 
            border: none;
            text-transform: uppercase;
            box-shadow: 0 0 10px #00ff00; 
        }
        .btn-danger { 
            background-color: red !important; 
            color: white !important; 
            border: none;
            box-shadow: 0 0 10px red;
        }
        
        /* 6. OCULTAR. */
        button[type="reset"] { display: none !important; }

        /* 7. TABLA DEL RANKING */
        table, tr, td, th, .table {
            background-color: transparent !important; /* Fondo transparente */
            color: white !important; /* Texto blanco */
            border-color: gold !important; /* Líneas doradas */

        label { color: #00ff00 !important; font-weight: bold; font-size: 16px; }
        .close { color: white !important; opacity: 1; }
        
        /* Ocultar scroll */
        body { overflow-x: hidden; }
    </style>
    """)

# Esto evita que el juego falle si se usa el nombre repetido
inyectar_estilo_transparente = inyectar_estilos_nucleares 

def mostrar_enemigo(clave_imagen, nombre, color):
    """
    Muestra la imagen del enemigo centrada y con marco de color.
    """
    with put_column().style('display: flex; flex-direction: column; align-items: center; margin: 20px 0;'):
        img = IMAGENES.get(clave_imagen)
        
        if img:
            # Imagen con borde neón del color del nivel
            put_image(img, width='250px').style(f'''
                background: white; 
                border: 4px solid white; 
                border-radius: 15px; 
                box-shadow: 0 0 30px {color};
            ''')
        else:
            put_text("[IMAGEN NO ENCONTRADA]").style('color: red;')

        # Nombre del enemigo
        put_text(nombre).style(f'''
            background: black; 
            color: {color}; 
            padding: 8px 20px; 
            border: 2px solid {color}; 
            border-radius: 8px; 
            margin-top: 15px; 
            font-family: monospace; 
            font-weight: bold; 
            font-size: 18px;
            text-transform: uppercase;
            box-shadow: 0 0 10px {color};
        ''')

def sistema_audio():
    """
    Reproductor de música.
    """
    try:
        with open(ARCHIVO_AUDIO, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            src = f"data:audio/mp3;base64,{b64}"
            
            # Usamos dobles llaves {{ }} para que Python no se confunda con el JS
            audio_html = f"""
            <div style="position: fixed; top: 10px; right: 10px; z-index: 9999;">
                <audio id="musica" loop autoplay>
                    <source src="{src}" type="audio/mp3">
                </audio>
                <button onclick="var a=document.getElementById('musica'); if(a.paused) a.play(); else a.pause();" 
                        style="background:black; color:#0f0; border:2px solid #0f0; border-radius:50%; width:40px; height:40px; font-size:20px; cursor:pointer;">
                    🔊
                </button>
                <script>
                    var a = document.getElementById("musica");
                    a.volume = 0.3;
                    document.addEventListener('click', function() {{ a.play(); }}, {{once:true}});
                </script>
            </div>
            """
            
            run_js(f"""
            if(!document.getElementById('musica')) {{
                var d = document.createElement('div');
                d.innerHTML = `{audio_html}`;
                document.body.appendChild(d);
            }}
            """)
    except:
        pass

# --- 5. RANKING ---

def guardar_ranking(nombre, xp):
    """Guarda el puntaje en un archivo JSON local"""
    archivo = 'ranking.json'
    datos = []
    
    # 1. Intentamos leer el archivo si existe
    if os.path.exists(archivo):
        try:
            with open(archivo, 'r') as f: datos = json.load(f)
        except: pass
    
    # 2. Agregamos al jugador actual
    datos.append({"nombre": nombre, "xp": xp})
    
    # 3. Ordenamos: Mayor XP arriba y cortamos para dejar solo el Top 10
    datos = sorted(datos, key=lambda x: x['xp'], reverse=True)[:5]
    
    # 4. Guardamos de nuevo
    with open(archivo, 'w') as f: json.dump(datos, f)

def ver_ranking():
    """Muestra la tabla de líderes"""
    clear()
    inyectar_estilos_nucleares()
    
    # Fondo desaturado para que resalte la tabla
    put_image(IMAGENES['base']).style('position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1; filter: grayscale(1);')
    
    archivo = 'ranking.json'
    filas = []
    
    # Leemos los datos
    if os.path.exists(archivo):
        try:
            with open(archivo, 'r') as f:
                lista = json.load(f)
                for idx, entry in enumerate(lista):
                    # Decoración para los 3 primeros lugares
                    rango = f"#{idx+1}"
                    if idx == 0: rango = "🥇 REY DEL HACKEO"
                    if idx == 1: rango = "🥈 LEYENDA"
                    if idx == 2: rango = "🥉 MAESTRO"
                    
                    filas.append([rango, entry['nombre'], entry['xp']])
        except: pass
            
    # Dibujamos la tabla
    with put_column().style('background: rgba(0,0,0,0.95); padding: 30px; border: 2px solid gold; border-radius: 15px; max-width: 600px; margin: 10vh auto; text-align: center; box-shadow: 0 0 50px rgba(255, 215, 0, 0.3);'):
        put_html("<h1 style='color: gold; font-family: monospace; text-shadow: 0 0 10px gold;'>🏆 SALÓN DE LA FAMA</h1>")
        
        if filas:
            put_table(filas, header=['Rango', 'Agente', 'XP Final']).style('color: white; font-size: 18px; width: 100%;')
        else:
            put_text("Aún no hay registros. ¡Sé el primero!").style('color: white; font-style: italic;')
        
        put_button("VOLVER AL MENÚ", onclick=mapa_principal).style('margin-top: 20px; background: gold; color: black; font-weight: bold; width: 100%;')

# --- 6. LOGICA PRINCIPAL ---

def iniciar_mision_maestra(tipo_nivel):
    # Configuración de niveles
    configs = {
        'fiesta': {'fondo': 'fiesta', 'img': 'enemigo_fiesta', 'nom': 'ENEMIGO: ALCOHOL', 'col': '#00ff00'},
        'vape': {'fondo': 'bano', 'img': 'enemigo_vape', 'nom': 'ENEMIGO: VAPE', 'col': '#00ff00'},
        'adulterado': {'fondo': 'mercado', 'img': 'enemigo_adulterado', 'nom': '¡ALERTA METANOL!', 'col': 'red'},
        'coca': {'fondo': 'callejon', 'img': 'enemigo_coca', 'nom': '¡TAQUICARDIA!', 'col': 'yellow'},
        'marihuana': {'fondo': 'parque', 'img': 'enemigo_marihuana', 'nom': 'ENEMIGO: THC', 'col': '#00ff00'},
        'tusi': {'fondo': 'vip', 'img': 'enemigo_tusi', 'nom': 'CÓCTEL TÓXICO', 'col': '#ff00ff'},
        'fentanilo': {'fondo': 'laboratorio', 'img': 'enemigo_fentanilo', 'nom': 'PELIGRO MORTAL', 'col': '#00ffff'},
        'farmacos': {'fondo': 'botiquin', 'img': 'enemigo_farmacos', 'nom': 'ADICCIÓN SILENCIOSA', 'col': '#ffa500'}
    }
    
    datos = configs[tipo_nivel]
    
    img_fondo = IMAGENES[datos['fondo']] if IMAGENES[datos['fondo']] else IMAGENES['base']
    
    # Selección de preguntas
    pregunta_obj = random.choice(DB_PREGUNTAS[tipo_nivel])
    opciones = pregunta_obj['falsas'] + [pregunta_obj['correcta']]
    random.shuffle(opciones)
    
    clear()
    inyectar_estilo_transparente()
    put_image(img_fondo).style('position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;')
    
    mostrar_enemigo(datos['img'], datos['nom'], datos['col'])

    with put_column().style('max-width: 600px; margin: 0 auto;'):
        res = input_group("⚔️ BATALLA TÁCTICA", [radio(pregunta_obj['p'], options=opciones, name='r')])
    
    if res['r'] == pregunta_obj['correcta']:
        jugador['xp'] += 100
        jugador['misiones'].append(tipo_nivel)
        toast("¡CORRECTO! +100 XP", color='success')
        
        clear()
        inyectar_estilo_transparente()
        put_image(IMAGENES['base']).style('position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;')
        with put_column().style('background: rgba(0,20,0,0.9); border: 2px solid #0f0; padding: 30px; border-radius: 10px; max-width: 500px; margin: 20vh auto; text-align: center;'):
            put_html("<h1 style='color: #0f0;'>AMENAZA NEUTRALIZADA</h1>")
            put_text(pregunta_obj['info']).style('color: white; margin: 20px 0; font-style: italic;')
            put_button("CONTINUAR", onclick=mapa_principal).style('background: #0f0; color: black;')
    else:
        jugador['vida'] -= 30
        popup("❌ ERROR DE SISTEMA", [
            put_text("Respuesta incorrecta.").style('color: red; font-weight: bold;'),
            put_markdown(f"**Correcta:** {pregunta_obj['correcta']}"),
            put_html("<hr>"),
            put_text(pregunta_obj['info']),
            put_buttons(['ENTENDIDO'], onclick=lambda _: close_popup())
        ])
        if jugador['vida'] <= 0: pantalla_game_over("Salud crítica.")
        else: mapa_principal()

def zona_jefe():
    global jugador
    
    # 1. Recuperación de vida
    if jugador['vida'] < 100:
        jugador['vida'] = 100
        toast("❤️ SALUD RESTAURADA AL 100%", color='success')
        time.sleep(2)

    vida_jefe = 3
    
    # 2. Las Preguntas
    trampas = [
        {"p": "Tienes 'Tolerancia Alta'. Bebes el doble sin sentirte mal. ¿Qué pasa en tu cuerpo?", "correcta": "Peligro de sobredosis silenciosa.", "falsas": ["Soy más fuerte.", "Controlo la sustancia."], "retro": "Tu cerebro se adormece, pero tu hígado recibe el doble de daño."},
        {"p": "Mezcla: Alcohol + Pastillas para dormir. ¿Resultado?", "correcta": "Efecto multiplicado (Mortal).", "falsas": ["Se suman.", "Se anulan."], "retro": "1+1=10. La mezcla potencia el efecto depresor y puede parar tu respiración."},
        {"p": "'Solo consumo el fin de semana y trabajo bien'. ¿Soy adicto?", "correcta": "Posiblemente (Adicción Funcional).", "falsas": ["No, porque trabajo.", "No, si no es diario."], "retro": "La adicción se mide por la ansiedad al dejarlo, no por si trabajas."},
        {"p": "Hongo venenoso 100% natural vs Pastilla. ¿Lo natural es seguro?", "correcta": "No, el veneno es veneno.", "falsas": ["Sí, es medicina.", "El cuerpo lo acepta mejor."], "retro": "El cianuro es natural. El origen no define la seguridad."},
        {"p": "¿Quién sufre más daño cerebral permanente?", "correcta": "El adolescente.", "falsas": ["El adulto.", "Igual."], "retro": "Tu cerebro está en desarrollo hasta los 25 años. El daño es irreversible."}
    ]

    # 3. Bucle de Batalla
    while vida_jefe > 0 and jugador['vida'] > 0:
        
        # Selección de pregunta
        pregunta = random.choice(trampas)
        opciones = [{'label': txt, 'value': 'mal'} for txt in pregunta['falsas']]
        opciones.append({'label': pregunta['correcta'], 'value': 'bien'})
        random.shuffle(opciones)
        
        # --- RENDERIZADO DE LA PREGUNTA ---
        clear()
        inyectar_estilos_nucleares()
        
        # Cargar imágenes
        fondo_usar = IMAGENES.get('fondo_jefe') if IMAGENES.get('fondo_jefe') else IMAGENES['base']
        put_image(fondo_usar).style('position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;')
        
        clave_imagen_jefe = 'jefe' if IMAGENES.get('jefe') else 'enemigo_fiesta'
        mostrar_enemigo(clave_imagen_jefe, f"JEFE FINAL (VIDA: {vida_jefe})", "red")
        
        # Espaciado adicional entre enemigo y pregunta
        put_html('<div style="height: 50px;"></div>')
        
        # Mostrar pregunta y ESPERAR respuesta
        with put_column().style('max-width: 600px; margin: 0 auto; padding: 0 20px;'):
            res = actions(pregunta['p'], buttons=opciones)
        
        # --- LÓGICA DE RESULTADO ---
        clear() # Borramos la pregunta
        inyectar_estilos_nucleares()
        put_image(fondo_usar).style('position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1; filter: brightness(0.3);') # Fondo más oscuro para leer
        
        if res == 'bien':
            vida_jefe -= 1
            # Pantalla de Éxito que BLOQUEA hasta dar clic
            if vida_jefe > 0:
                with put_column().style('text-align: center; margin-top: 20vh; max-width: 600px; margin-left: auto; margin-right: auto;'):
                    put_html("<h1 style='color: #0f0; font-size: 50px;'>💥 ¡GOLPE EXITOSO!</h1>")
                    put_markdown(f"### VERDAD DESBLOQUEADA:\n{pregunta['retro']}").style('color: white; font-size: 20px; border: 2px solid #0f0; padding: 20px; border-radius: 10px; background: rgba(0,0,0,0.8);')
                    # Este 'actions' hace que el código se DETENGA aquí hasta dar clic
                    actions(buttons=['🤜 SIGUIENTE ATAQUE'])
                
        else:
            jugador['vida'] -= 40
            # Pantalla de Fallo que BLOQUEA hasta dar clic
            with put_column().style('text-align: center; margin-top: 20vh; max-width: 600px; margin-left: auto; margin-right: auto;'):
                put_html("<h1 style='color: red; font-size: 50px;'>💔 TE HIZO DAÑO</h1>")
                put_markdown(f"### LA REALIDAD ES:\n{pregunta['retro']}").style('color: white; font-size: 20px; border: 2px solid red; padding: 20px; border-radius: 10px; background: rgba(0,0,0,0.8);')
                # Este 'actions' hace que el código se DETENGA aquí
                actions(buttons=['🤕 RECUPERARSE Y SEGUIR'])

    # Fin del juego
    if jugador['vida'] > 0:
        pantalla_victoria()
    else:
        pantalla_game_over("El sistema te venció.")

# --- 7. FLUJO ---
def bienvenida():
    # Reiniciar todo
    jugador['xp'] = 0
    jugador['vida'] = 100
    jugador['misiones'] = []
    
    clear()
    inyectar_estilo_transparente()
    sistema_audio()   
    
    put_image(IMAGENES['portada']).style('position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1; filter: brightness(0.6);')
    put_column([
        put_html("<h1 style='font-family: monospace; color: white; text-shadow: 0 0 10px #0f0; font-size: 50px; text-align: center;'>🕵️ NEURO-DEFENDERS</h1>"),
        put_text("/// HACKEA LOS MITOS ///").style('color: #0f0; background: rgba(0,0,0,0.5); font-family: monospace;'),
        put_button("INICIAR MISIÓN [▶]", onclick=crear_perfil).style('margin-top: 20px; border: 2px solid #0f0; background: black; color: #0f0;')
    ]).style('height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center;')

def crear_perfil():
    clear()
    inyectar_estilo_transparente()
    put_image(IMAGENES['registro']).style('position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;')
    
    def validar_nombre(n):
        if not n: return "El nombre es obligatorio"
        if len(n) > 10: return "Máximo 10 caracteres"

    # Contenedor con margen superior fijo
    with put_column().style('margin-top: 15vh; padding: 20px; max-width: 600px; margin-left: auto; margin-right: auto;'):
        data = input_group("REGISTRO", [input("NICKNAME:", name='nombre', validate=validar_nombre), radio("CLASE:", ['🧬 BIO-HACKER', '🛡️ TÁCTICO'], name='clase')])
    jugador['nombre'] = data['nombre']
    mapa_principal()

def mapa_principal():
    clear()
    inyectar_estilo_transparente()
    put_image(IMAGENES['base']).style('position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1; filter: brightness(0.5);')
    
    put_row([
        put_text(f"👤 {jugador['nombre']}"), put_text(f"🏆 XP: {jugador['xp']}"), put_text(f"❤️ {jugador['vida']}%")
    ]).style('background: rgba(0,20,0,0.9); color: #0f0; padding: 10px; font-weight: bold; justify-content: space-around; border-bottom: 2px solid #0f0;')
    
    put_markdown("## 📡 SELECCIONA OBJETIVO:").style('text-align: center; color: white; margin-top: 50px;')
    
    botones = []
    if 'fiesta' not in jugador['misiones']: botones.append(put_button("🍺 LA FIESTA", onclick=lambda: iniciar_mision_maestra('fiesta')))
    if 'vape' not in jugador['misiones']: botones.append(put_button("💨 EL BAÑO (Vape)", onclick=lambda: iniciar_mision_maestra('vape')))
    if 'adulterado' not in jugador['misiones']: botones.append(put_button("☠️ MERCADO (Adulterado)", onclick=lambda: iniciar_mision_maestra('adulterado')))
    if 'coca' not in jugador['misiones']: botones.append(put_button("⚡ CALLEJÓN (Cocaína)", onclick=lambda: iniciar_mision_maestra('coca')))
    if 'marihuana' not in jugador['misiones']: botones.append(put_button("🌿 PARQUE (Marihuana)", onclick=lambda: iniciar_mision_maestra('marihuana')))
    if 'fentanilo' not in jugador['misiones']: botones.append(put_button("🧪 LABORATORIO (Fentanilo)", onclick=lambda: iniciar_mision_maestra('fentanilo')))
    if 'tusi' not in jugador['misiones']: botones.append(put_button("💎 ZONA VIP (Tusi)", onclick=lambda: iniciar_mision_maestra('tusi')))
    if 'farmacos' not in jugador['misiones']: botones.append(put_button("💊 FARMACIA (Fármacos)", onclick=lambda: iniciar_mision_maestra('farmacos')))
    
    if len(jugador['misiones']) >= 8:
        put_error("⚠️ ¡JEFE FINAL DISPONIBLE!").style('text-align: center;')
        botones.append(put_button("👹 ENFRENTAR PRESIÓN SOCIAL", onclick=zona_jefe, color='danger'))
    
    botones.append(put_button("🏆 VER RANKING", onclick=ver_ranking, color='warning'))
    put_column(botones).style('max-width: 500px; margin: 0 auto;')

# --- PARTE FINAL DE LA SECCIÓN 7 ---

def pantalla_victoria():
    # 1. GUARDAMOS EL PUNTAJE AUTOMÁTICAMENTE
    guardar_ranking(jugador['nombre'], jugador['xp'])
    
    clear()
    inyectar_estilos_nucleares()
    put_image(IMAGENES['base']).style('position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;')
    
    with put_column().style('text-align: center; margin-top: 10vh; padding: 0 20px;'):
        put_html("<h1 style='color: gold; font-size: 60px; text-shadow: 0 0 20px gold;'>🏆 ¡VICTORIA TOTAL!</h1>")
        
        # Mostramos el trofeo centrado
        with put_column().style('display: flex; align-items: center; justify-content: center; margin: 20px 0;'):
            put_image(IMAGENES['trofeo'], width='200px').style('filter: drop-shadow(0 0 15px gold); display: block; margin: 0 auto;')
        
        # Resumen
        put_html(f"""
        <div style="background: black; border: 2px solid gold; padding: 20px; border-radius: 10px; margin: 20px auto; max-width: 400px;">
            <h2 style="color: white; margin:0;">AGENTE: {jugador['nombre']}</h2>
            <h1 style="color: gold; font-size: 40px; margin: 10px 0;">XP: {jugador['xp']}</h1>
        </div>
        """)
        
        # Botones finales
        put_row([
            put_button("📜 VER PODIO", onclick=ver_ranking, color='warning').style('margin-right: 10px;'),
            put_button("🔄 JUGAR DE NUEVO", onclick=lambda: run_js('location.reload()'), color='success')
        ], size='auto').style('justify-content: center; margin-top: 20px;')
        
        # Descarga de PDF
        try:
            content = open(ARCHIVO_PDF, 'rb').read()
            put_file('info_prevencion.pdf', content, '📥 DESCARGAR GUÍA (PDF)').style('display: block; margin-top: 20px;')
        except: pass

def pantalla_game_over(razon):
    # TAMBIÉN GUARDAMOS AL PERDER
    guardar_ranking(jugador['nombre'], jugador['xp'])
    
    clear()
    inyectar_estilos_nucleares()
    put_image(IMAGENES['game_over']).style('position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;')
    
    with put_column().style('text-align: center; margin-top: 20vh; background: rgba(0,0,0,0.9); padding: 30px; border: 2px solid red; border-radius: 15px; box-shadow: 0 0 30px red;'):
        put_html(f"<h1 style='color: red; font-size: 50px;'>💀 MISIÓN FALLIDA</h1>")
        put_text(razon).style('color: white; font-size: 20px; margin-bottom: 20px;')
        put_text(f"XP ACUMULADA: {jugador['xp']}").style('color: yellow; font-weight: bold;')
        
        put_row([
            put_button("📜 VER PODIO", onclick=ver_ranking, color='warning').style('margin-right: 10px;'),
            put_button("💀 REINTENTAR", onclick=lambda: run_js('location.reload()'), color='danger')
        ], size='auto').style('justify-content: center; margin-top: 20px;')


if __name__ == '__main__':
    # Configuración dinámica de puerto para Render
    port = int(os.environ.get('PORT', 8080))
    start_server(bienvenida, port=port, theme='dark')