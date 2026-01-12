from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
from pywebio.session import run_js
import time

# --- CONFIGURACIÓN DE IMÁGENES ---
IMAGENES = {
    # Fondos
    'mapa': open('portada_neoquito.png', 'rb').read(),
    'registro_fondo': open('registro_fondo.png', 'rb').read(),
    'fondo_misiones': open('fondo_misiones.png', 'rb').read(),
    'fondo_fiesta': open('fondo_fiesta.png', 'rb').read(),
    'fondo_bano': open('fondo_bano.png', 'rb').read(),
    'fondo_mercado': open('fondo_mercado.png', 'rb').read(),
    'fondo_callejon': open('fondo_callejon.png', 'rb').read(),
    
    # Enemigos 
    'enemigo_fiesta': open('enemigo_fiesta.png', 'rb').read(),
    'enemigo_vape': open('enemigo_vape.png', 'rb').read(),
    'enemigo_adulterado': open('enemigo_adulterado.png', 'rb').read(),
    'enemigo_coca': open('enemigo_coca.png', 'rb').read(),
    
    # Extras
    'trofeo': open('trofeo.png', 'rb').read(),
    'game_over': open('game_over.png', 'rb').read()
}

# --- VARIABLES GLOBALES ---
jugador = {
    "nombre": "",
    "clase": "",
    "xp": 0,
    "vida": 100,
    "misiones_completadas": [],
    "powerup_usado": False
}

def validar_nombre(nombre):
    if len(nombre) > 10: return '¡Muy largo! Max 10 letras.'
    if not nombre: return 'Escribe algo.'

# --- 1. BIENVENIDA ---
def bienvenida():
    clear()
    run_js("$('body').css({'margin': '0', 'padding': '0', 'overflow': 'hidden'});")
    put_image(IMAGENES['mapa']).style('position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1; filter: brightness(0.6);')

    put_column([
        put_html("""
        <style>
            @keyframes latido-neon { 0% { text-shadow: 0 0 5px #0f0; } 50% { text-shadow: 0 0 20px #0f0; } 100% { text-shadow: 0 0 5px #0f0; } }
            .titulo-juego { font-family: 'Courier New', monospace; font-size: 45px; font-weight: bold; color: white; animation: latido-neon 2s infinite; text-align: center; }
            .subtitulo { color: #0f0; font-family: monospace; background: rgba(0,0,0,0.5); padding: 5px; }
        </style>
        <div class="titulo-juego">🕵️ NEURO-DEFENDERS v4.0</div>
        <div class="subtitulo">/// Misión: Hackear los mitos en Neo-Quito ///</div>
        """),
        put_button("INICIAR SISTEMA [▶]", onclick=crear_perfil).style('font-size: 20px; padding: 15px 30px; border: 2px solid #0f0; background-color: black; color: #0f0;')
    ]).style('height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center;')

# --- 2. PERFIL ---
def crear_perfil():
    clear()
    put_image(IMAGENES['registro_fondo']).style('position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;')

    put_html("""
    <style>
        body, html, #pywebio-scope-root, .container, .main, .footer, div, .row, .col {
            background: transparent !important;
            background-color: transparent !important;
            box-shadow: none !important;
        }
        .card {
            background-color: rgba(0, 0, 0, 0.9) !important;
            border: 2px solid #00ff00 !important;
            box-shadow: 0 0 30px #00ff00;
            max-width: 500px !important;
            margin: 20vh auto !important;
            border-radius: 10px;
            padding: 20px;
        }
        .card-header, button[type="reset"] { display: none !important; }
        label, .form-check-label { color: #00ff00 !important; font-family: monospace; font-weight: bold; text-transform: uppercase; }
        .form-control { background-color: #001100 !important; color: white !important; border: 1px solid #00ff00 !important; }
        .invalid-feedback { color: #ffff00 !important; font-weight: bold; font-family: monospace; }
        button[type="submit"] {
            background-color: #00ff00 !important;
            color: black !important;
            font-weight: bold;
            border: none;
            width: 100%;
            font-size: 0 !important;
            margin-top: 15px;
        }
        button[type="submit"]:after { content: "▶ COMENZAR MISIÓN"; font-size: 18px; letter-spacing: 2px; }
    </style>
    """)

    def chequear_clase(val):
        if not val: return "⚠️ Por favor, selecciona una clase."

    datos = input_group("", [
        input("NOMBRE CLAVE (NICK):", name='nombre', validate=validar_nombre, placeholder="Escribe tu alias..."),
        radio("SELECCIONA TU CLASE:", options=['🧬 BIO-HACKER (Inteligencia)', '🛡️ TÁCTICO (Resistencia)'], name='clase', validate=chequear_clase)
    ])
    
    jugador['nombre'] = datos['nombre']
    jugador['clase'] = datos['clase'].split(" ")[1] 
    
    toast(f"IDENTIDAD CONFIRMADA: {jugador['nombre']}", color='success')
    time.sleep(1) 
    mapa_principal()

# --- 3. MAPA PRINCIPAL ---
def mapa_principal():
    clear()
    put_image(IMAGENES['fondo_misiones']).style('position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1; filter: brightness(0.5);')

    put_html("""
    <style>
        body, html, .content, .container, .main, .footer, #pywebio-scope-root { background: transparent !important; }
        .hud-bar { background: rgba(0, 20, 0, 0.9); border-bottom: 2px solid #0f0; padding: 15px; display: flex; justify-content: space-around; color: white; font-family: monospace; font-size: 18px; }
        .dato-hud { color: #00ff00; font-weight: bold; }
        button { background: rgba(0,0,0,0.8) !important; border: 2px solid #0f0 !important; color: #0f0 !important; font-family: monospace !important; padding: 15px !important; margin: 10px 0 !important; width: 100% !important; text-align: left !important; }
        button:hover { background: #0f0 !important; color: black !important; box-shadow: 0 0 20px #0f0 !important; }
    </style>
    """)

    put_html(f"""
    <div class="hud-bar">
        <span>👤 AGENTE: <span class="dato-hud">{jugador['nombre']}</span></span>
        <span>🏆 XP: <span class="dato-hud">{jugador['xp']}</span></span>
        <span>❤️ SALUD: <span class="dato-hud">{jugador['vida']}%</span></span>
    </div>
    """)

    put_markdown("## 📡 SELECCIONA TU OBJETIVO:").style('text-align: center; color: white; text-shadow: 0 0 10px #0f0;')

    lista_botones = []
    
    if len(jugador['misiones_completadas']) >= 4:
        put_error("⚠️ ¡JEFE FINAL DETECTADO!").style('text-align: center; background: transparent;')
        lista_botones.append(put_button("💀 ENFRENTAR PRESIÓN SOCIAL", onclick=lambda: zona_jefe(), color='danger').style('border-color: red !important; color: white !important; box-shadow: 0 0 30px red !important;'))
    else:
        if 'fiesta' not in jugador['misiones_completadas']:
            lista_botones.append(put_button("🍺 LA FIESTA (Alcohol)", onclick=lambda: zona_fiesta()))
        if 'vape' not in jugador['misiones_completadas']:
            lista_botones.append(put_button("💨 EL BAÑO (Vape)", onclick=lambda: zona_vape()))
        if 'adulterado' not in jugador['misiones_completadas']:
            lista_botones.append(put_button("☠️ MERCADO NEGRO (Adulterado)", onclick=lambda: zona_adulterado()))
        if 'coca' not in jugador['misiones_completadas']:
            lista_botones.append(put_button("⚡ EL CALLEJÓN (Cocaína)", onclick=lambda: zona_coca()))
        if not jugador['powerup_usado']:
            lista_botones.append(put_button("💾 DESCARGAR DATOS (+XP)", onclick=lambda: usar_powerup()).style('border-color: yellow !important; color: yellow !important;'))

    put_column(lista_botones).style('max-width: 600px; margin: 0 auto;')


# --- CSS MISIONES (ESTILO EVIDENCIA/STICKER) ---
def css_misiones():
    put_html("""
    <style>
        body, html, #pywebio-scope-root, .container, .main, .footer, div, .row, .col {
            background: transparent !important;
            background-color: transparent !important;
            box-shadow: none !important;
        }
        
        /* CAJA DE PREGUNTA */
        .card {
            background-color: rgba(0, 0, 0, 0.9) !important;
            border: 2px solid #00ff00 !important;
            box-shadow: 0 0 20px #00ff00;
            color: white !important;
            border-radius: 10px;
            max-width: 450px !important;
            margin-top: 20px !important;
            margin-bottom: 50px !important;
}
        }
        
        .card-header { 
            background: transparent !important; 
            color: #00ff00 !important; 
            font-family: monospace; 
            font-weight: bold;
            border-bottom: 1px dashed #0f0 !important;
        }
        
        .form-check-label { color: white !important; font-family: monospace; font-size: 16px; }
        
        button[type="submit"] {
            background: #00ff00 !important;
            color: black !important;
            font-weight: bold;
            text-transform: uppercase;
            width: 100%;
            margin-top: 10px;
        }
        button[type="reset"] { display: none !important; }

        /* CONTENEDOR DEL ENEMIGO */
        .marco-enemigo {
            background: transparent;
            text-align: center;
            max-width: 400px;
            margin: 0 auto 20px auto;
        }
        
        /* ESTILO PARA LA IMAGEN (El truco para el fondo blanco) */
        .marco-enemigo img {
            border-radius: 15px;
            border: 3px solid white;
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.5);
            background-color: white;
        }
        
        /* ETIQUETA DEL NOMBRE */
        .marco-enemigo span {
            display: block;
            margin-top: 10px;
            background-color: rgba(0,0,0,0.8);
            padding: 5px;
            border-radius: 5px;
            border: 1px solid #00ff00;
            color: #00ff00;
            font-family: monospace;
            font-weight: bold;
        }
    </style>
    """)


# --- MISIONES (LÓGICA) ---

def usar_powerup():
    clear()
    put_image(IMAGENES['fondo_misiones']).style('position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;')
    css_misiones()
    
    put_markdown("## 💾 DESCARGANDO BASE DE DATOS...")
    with put_loading(): time.sleep(1.5)
    
    # REPORTE DE DATOS
    clear()
    put_image(IMAGENES['fondo_misiones']).style('position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;')
    css_misiones()
    
    with put_column().style('background: rgba(0,0,0,0.9); border: 2px solid yellow; padding: 20px; border-radius: 10px; max-width: 500px; margin: 15vh auto; text-align: center;'):
        put_html("<h2 style='color: yellow;'>💾 DATOS OBTENIDOS</h2>")
        put_markdown("""
        * **Dato 1:** El cerebro adolescente es 5 veces más propenso a la adicción.
        * **Dato 2:** En Ecuador, el consumo empieza a los 12 años.
        """)
        put_text("+50 XP AÑADIDOS").style('color: #0f0; font-weight: bold;')
        put_button("VOLVER AL MAPA", onclick=mapa_principal).style('background: yellow !important; color: black !important;')

    jugador['xp'] += 50
    jugador['powerup_usado'] = True

def zona_fiesta():
    clear()
    put_image(IMAGENES['fondo_fiesta']).style('position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;')
    css_misiones()
    
    # --- CAMBIO REALIZADO: Borramos lo viejo y llamamos a la función nueva ---
    mostrar_enemigo_centrado('enemigo_fiesta', 'ENEMIGO: ALCOHOL', '#00ff00')
    # -------------------------------------------------------------------------

    res = input_group("🍺 RONDA 1/2", [
        radio("Mito: 'La cerveza no emborracha'.", ['A) Verdad.', 'B) Falso, es igual.'], name='r')
    ])
    check_ronda(res['r'].startswith('B'), 30)
    
    # ... (el resto de la función sigue igual) ...
    time.sleep(1)
    clear()
    put_image(IMAGENES['fondo_fiesta']).style('position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;')
    css_misiones()
    
    res2 = input_group("🍺 RONDA FINAL", [
        radio("Efecto en cerebro:", ['A) Mata neuronas.', 'B) Relaja.'], name='r')
    ])
    finalizar_mision(res2['r'].startswith('A'), 'fiesta', 100)


def zona_vape():
    clear()
    put_image(IMAGENES['fondo_bano']).style('position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;')
    css_misiones()
    
    # --- CAMBIO REALIZADO ---
    mostrar_enemigo_centrado('enemigo_vape', 'ENEMIGO: VAPE', '#00ff00')
    # ------------------------
    
    res = input_group("💨 RONDA 1/2", [
        radio("'Es solo vapor...'", ['A) Falso, metales pesados.', 'B) Verdad.'], name='r')
    ])
    check_ronda(res['r'].startswith('A'), 30)
    
    # ... (el resto sigue igual) ...
    time.sleep(1)
    clear()
    put_image(IMAGENES['fondo_bano']).style('position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;')
    css_misiones()
    
    res2 = input_group("💨 RONDA FINAL", [
        radio("¿Qué es EVALI?", ['A) Marca.', 'B) Enfermedad mortal.'], name='r')
    ])
    finalizar_mision(res2['r'].startswith('B'), 'vape', 100)

def zona_adulterado():
    clear()
    put_image(IMAGENES['fondo_mercado']).style('position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;')
    css_misiones()
    
    # --- CAMBIO REALIZADO ---
    mostrar_enemigo_centrado('enemigo_adulterado', '¡ALERTA METANOL!', 'red')
    # ------------------------
    
    res = input_group("☠️ ELIGE", [
        radio("Consecuencia:", ['A) Ceguera/Muerte.', 'B) Dolor leve.'], name='r')
    ])
    finalizar_mision(res['r'].startswith('A'), 'adulterado', 150)


def zona_coca():
    clear()
    put_image(IMAGENES['fondo_callejon']).style('position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;')
    css_misiones()
    
    # --- CAMBIO REALIZADO ---
    mostrar_enemigo_centrado('enemigo_coca', '¡TAQUICARDIA!', 'yellow')
    # ------------------------
    
    res = input_group("⚡ ELIGE", [
        radio("Efecto real:", ['A) Energía.', 'B) Infarto/Paranoia.'], name='r')
    ])
    finalizar_mision(res['r'].startswith('B'), 'coca', 200)


def zona_jefe():
    clear()
    put_image(IMAGENES['fondo_misiones']).style('position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;')
    css_misiones()
    
    put_markdown("# 👹 PRESIÓN SOCIAL").style('text-align: center; background: black; color: red;')
    
    res = input_group("TUS AMIGOS INSISTEN...", [
        radio("¿QUÉ HACES?", ['A) Acepto.', 'B) Digo NO y me voy.'], name='r')
    ])
    
    if res['r'].startswith('B'):
        jugador['xp'] += 500
        pantalla_victoria()
    else:
        pantalla_game_over("Caíste en la presión social.")

# --- HELPERS ---

def mostrar_enemigo_centrado(clave_imagen, nombre, color_neon):
    """
    Muestra al enemigo estilo STICKER, centrado, pero MAS ARRIBA para que quepa la pregunta.
    """
    # 1. Activamos el scroll por si acaso la pantalla es muy pequeña
    run_js("$('body').css('overflow', 'auto');")

    # 2. margin-top: 20px (antes era 10vh). Esto sube la imagen casi hasta arriba.
    with put_column().style('display: flex; flex-direction: column; align-items: center; justify-content: center; margin-top: 20px; margin-bottom: 20px;'):
        
        # IMAGEN
        put_image(IMAGENES[clave_imagen], width='250px').style(f'''
            background: white; 
            border: 4px solid white; 
            border-radius: 15px; 
            box-shadow: 0 0 25px {color_neon};
        ''')
        
        # TEXTO
        put_text(nombre).style(f'''
            background: black; 
            color: {color_neon}; 
            padding: 8px 20px; 
            border: 2px solid {color_neon}; 
            border-radius: 8px; 
            margin-top: 15px; 
            font-family: monospace; 
            font-weight: bold; 
            font-size: 18px;
            text-transform: uppercase;
            box-shadow: 0 0 10px {color_neon};
        ''')

def check_ronda(gano, dano):
    if gano: toast("¡Correcto! ✅", color='success')
    else:
        jugador['vida'] -= dano
        toast(f"¡Daño! -{dano}", color='error')
        if jugador['vida'] <= 0: pantalla_game_over("Salud crítica.")

def finalizar_mision(gano, id_mision, xp):
    clear()
    # Usamos fondo_misiones por simplicidad, pero podrías usar el de la zona específica
    put_image(IMAGENES['fondo_misiones']).style('position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;')
    css_misiones()
    
    if gano:
        jugador['xp'] += xp
        jugador['misiones_completadas'].append(id_mision)
        
        with put_column().style('background: rgba(0,0,0,0.95); border: 2px solid #0f0; padding: 30px; border-radius: 10px; max-width: 500px; margin: 20vh auto; text-align: center; box-shadow: 0 0 30px #0f0;'):
            put_html("<h1 style='color: #0f0;'>🛡️ ZONA SEGURA</h1>")
            put_text(f"Has neutralizado la amenaza.").style('color: white; font-size: 18px;')
            put_html(f"<h2 style='color: yellow;'>GANASTE +{xp} XP</h2>")
            put_button("CONTINUAR", onclick=mapa_principal).style('width: 100%; margin-top: 20px;')
            
    else:
        jugador['vida'] -= 50
        with put_column().style('background: rgba(0,0,0,0.95); border: 2px solid red; padding: 30px; border-radius: 10px; max-width: 500px; margin: 20vh auto; text-align: center; box-shadow: 0 0 30px red;'):
            put_html("<h1 style='color: red;'>❌ FRACASO</h1>")
            put_text("El enemigo te ha intoxicado. Retirada táctica.").style('color: white; font-size: 18px;')
            put_html("<h3 style='color: red;'>DAÑO MASIVO RECIBIDO</h3>")
            
            if jugador['vida'] <= 0:
                put_button("VER ESTADO CRÍTICO", onclick=lambda: pantalla_game_over("Tu salud llegó a 0."))
            else:
                put_button("HUIR AL MAPA", onclick=mapa_principal, color='danger').style('width: 100%; margin-top: 20px;')

def pantalla_victoria():
    clear()
    put_image(IMAGENES['fondo_misiones']).style('position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;')
    css_misiones()
    
    with put_column().style('background: rgba(0,0,0,0.9); border: 4px solid gold; padding: 40px; border-radius: 15px; max-width: 600px; margin: 10vh auto; text-align: center; box-shadow: 0 0 50px gold;'):
        put_html("<h1 style='color: gold; font-size: 50px;'>🏆 ¡VICTORIA!</h1>")
        put_image(IMAGENES['trofeo'], width='200px').style('display:block; margin: 0 auto;')
        put_markdown(f"### AGENTE: {jugador['nombre']}").style('color: white;')
        put_html(f"<h2 style='color: #0f0;'>XP TOTAL: {jugador['xp']}</h2>")
        put_button("REINICIAR SISTEMA", onclick=bienvenida).style('margin-top: 20px; font-size: 20px;')

def pantalla_game_over(razon):
    clear()
    put_image(IMAGENES['fondo_misiones']).style('position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1; filter: grayscale(1);')
    css_misiones()
    
    with put_column().style('background: rgba(0,0,0,0.9); border: 4px solid red; padding: 40px; border-radius: 15px; max-width: 600px; margin: 10vh auto; text-align: center; box-shadow: 0 0 50px red;'):
        put_html("<h1 style='color: red; font-size: 50px;'>💀 GAME OVER</h1>")
        put_text(razon).style('color: white; font-size: 22px; margin: 20px 0;')
        put_button("REINTENTAR MISIÓN", onclick=bienvenida, color='danger').style('margin-top: 20px; font-size: 20px;')

if __name__ == '__main__':
    start_server(bienvenida, port=8080, theme='dark')