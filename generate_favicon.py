"""
Script para generar favicon.ico y apple-touch-icon.png desde favicon.svg
Requiere: pip install cairosvg pillow
"""

try:
    import cairosvg
    from PIL import Image
    import io

    # Rutas
    svg_path = "static/images/favicon.svg"
    ico_path = "static/images/favicon.ico"
    apple_path = "static/images/apple-touch-icon.png"

    # Generar favicon.ico (32x32)
    print("Generando favicon.ico...")
    png_data = cairosvg.svg2png(url=svg_path, output_width=32, output_height=32)
    image = Image.open(io.BytesIO(png_data))
    image.save(ico_path, format='ICO', sizes=[(32, 32)])
    print(f"✓ Creado: {ico_path}")

    # Generar apple-touch-icon.png (180x180)
    print("Generando apple-touch-icon.png...")
    png_data = cairosvg.svg2png(url=svg_path, output_width=180, output_height=180)
    image = Image.open(io.BytesIO(png_data))
    image.save(apple_path, format='PNG')
    print(f"✓ Creado: {apple_path}")

    print("\n¡Favicons generados exitosamente!")

except ImportError as e:
    print("Error: Faltan dependencias")
    print("\nInstala las dependencias con:")
    print("pip install cairosvg pillow")
    print("\nEn Windows, también necesitas GTK:")
    print("1. Descarga GTK de: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases")
    print("2. Instala GTK en tu sistema")
    print("\nO usa un generador online: https://realfavicongenerator.net/")

except Exception as e:
    print(f"Error al generar favicons: {e}")
    print("\nAlternativa: Usa un generador online")
    print("https://realfavicongenerator.net/")
