# Favicons - Rubi Perfumeria

## Archivos de Iconos

El archivo `favicon.svg` ya está creado con el diseño del icono de perfume.

### Para generar los archivos ICO y PNG:

**Opción 1: Usar un generador online**
1. Ve a https://realfavicongenerator.net/
2. Sube el archivo `favicon.svg`
3. Descarga el paquete de favicons generado
4. Copia los archivos a esta carpeta:
   - `favicon.ico` (32x32)
   - `apple-touch-icon.png` (180x180)

**Opción 2: Usar ImageMagick (línea de comandos)**
```bash
# Instalar ImageMagick primero
# En Windows: choco install imagemagick
# En Mac: brew install imagemagick
# En Linux: sudo apt install imagemagick

# Generar favicon.ico
magick convert favicon.svg -resize 32x32 favicon.ico

# Generar apple-touch-icon.png
magick convert favicon.svg -resize 180x180 apple-touch-icon.png
```

**Opción 3: Crear manualmente con herramientas de diseño**
- Usa Figma, Sketch, Photoshop, o GIMP
- Crea imágenes basadas en el diseño de `favicon.svg`
- Exporta en los siguientes tamaños:
  - favicon.ico: 32x32px
  - apple-touch-icon.png: 180x180px

## Colores del Diseño

- Gradiente: #E8DCC4 → #C9A961 (beige a dorado)
- Icono: #FFFFFF (blanco)

## Nota

El archivo SVG funciona perfectamente en navegadores modernos. Los archivos ICO y PNG son para compatibilidad con navegadores antiguos y dispositivos móviles.
