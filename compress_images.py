#!/usr/bin/env python3
"""
Script para comprimir imágenes PNG del juego NEURO-DEFENDERS
Reduce el tamaño de las imágenes manteniendo calidad visual aceptable
y poder usar el juego en render
"""

import os
from PIL import Image

def comprimir_imagen(ruta_entrada, ruta_salida=None, calidad=85, max_dimension=1920):
    """
    Comprime una imagen PNG
    
    Args:
        ruta_entrada: Path de la imagen original
        ruta_salida: Path donde guardar (None = sobrescribe original)
        calidad: Calidad de compresión (1-100)
        max_dimension: Dimensión máxima (ancho o alto)
    """
    if ruta_salida is None:
        ruta_salida = ruta_entrada
    
    try:
        img = Image.open(ruta_entrada)
        
        # Calcular nuevo tamaño manteniendo aspecto
        ancho, alto = img.size
        if ancho > max_dimension or alto > max_dimension:
            ratio = min(max_dimension/ancho, max_dimension/alto)
            nuevo_ancho = int(ancho * ratio)
            nuevo_alto = int(alto * ratio)
            img = img.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
        
        # Convertir RGBA a RGB si es necesario
        if img.mode == 'RGBA':
            fondo = Image.new('RGB', img.size, (0, 0, 0))
            fondo.paste(img, mask=img.split()[3])
            img = fondo
        
        # Guardar optimizado
        img.save(ruta_salida, 'PNG', optimize=True, quality=calidad)
        
        # Mostrar estadísticas
        tam_original = os.path.getsize(ruta_entrada)
        tam_nuevo = os.path.getsize(ruta_salida)
        reduccion = ((tam_original - tam_nuevo) / tam_original) * 100
        
        print(f"✓ {os.path.basename(ruta_entrada)}")
        print(f"  {tam_original/1024/1024:.2f}MB → {tam_nuevo/1024/1024:.2f}MB ({reduccion:.1f}% reducción)")
        
    except Exception as e:
        print(f"✗ Error con {ruta_entrada}: {e}")

def comprimir_todas_imagenes():
    """Comprime todas las imágenes PNG grandes del directorio"""
    
    # Lista de imágenes a comprimir
    imagenes_grandes = [
        'fondo_jefe.png',
        'fondo_botiquin.png',
        'fondo_vip.png',
        'fondo_laboratorio.png',
        'fondo_parque.png',
        'fondo_callejon.png',
        'fondo_fiesta.png',
        'fondo_mercado.png',
        'fondo_bano.png',
        'fondo_misiones.png',
        'registro_fondo.png',
        'portada_neoquito.png',
        'game_over.png',
        'trofeo.png',
        'enemigo_marihuana.png',
        'enemigo_fentanilo.png',
        'enemigo_vape.png',
        'enemigo_farmacos.png',
        'enemigo_coca.png',
        'enemigo_adulterado.png',
        'enemigo_fiesta.png',
        'enemigo_tusi.png',
        'jefe.png'
    ]
    
    print("🖼️  Comprimiendo imágenes...\n")
    
    for imagen in imagenes_grandes:
        if os.path.exists(imagen):
            comprimir_imagen(imagen)
        else:
            print(f"⚠️  No encontrada: {imagen}")
    
    print("\n✅ Compresión completada!")

if __name__ == '__main__':
    comprimir_todas_imagenes()
