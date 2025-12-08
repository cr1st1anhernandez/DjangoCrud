# Rubi Perfumeria - Sistema de Gestión Integral

## Documentación del Proyecto

### Cliente
**Rubi perfumeria**
Empresa dedicada a la comercialización de fragancias de alta gama, perfumes de diseñador y productos de cosmética premium.

### Alcance del Proyecto
Sistema integral de gestión de inventario, control de ventas y administración de productos para Rubi perfumeria, diseñado para optimizar las operaciones diarias del negocio y proporcionar herramientas de control empresarial.

---

## 1. Contexto del Negocio

### Necesidad del Cliente
Rubi perfumeria requería modernizar su sistema de gestión de inventario, eliminando procesos manuales y hojas de cálculo para implementar una solución digital robusta que permitiera:

- Control preciso del inventario de fragancias y productos de cosmética
- Trazabilidad completa de todas las operaciones
- Sistema de alertas para productos con stock crítico
- Gestión de múltiples usuarios con diferentes niveles de acceso
- Análisis de márgenes de ganancia por producto
- Registro de ventas y generación de tickets
- Control de roles (Administradores y Vendedores)

### Desafíos Identificados
1. Manejo de un catálogo extenso de productos con múltiples atributos (marca, género, tipo de fragancia, volumen)
2. Control de precios de compra y venta para cálculo de rentabilidad
3. Gestión de stock con alertas automáticas
4. Auditoría de cambios realizados por el personal
5. Sistema de punto de venta integrado
6. Interfaz intuitiva para personal no técnico

---

## 2. Requerimientos Funcionales

### 2.1 Gestión de Productos

#### Información del Producto
El sistema debe permitir registrar la siguiente información para cada producto:

**Datos Básicos:**
- Nombre del producto
- Marca (Dior, Chanel, Paco Rabanne, etc.)
- Descripción detallada

**Clasificación:**
- Categoría: Perfume, Eau de Toilette, Eau de Parfum, Eau de Cologne, Body Spray, Loción Corporal, Crema, Gel, Desodorante
- Género: Masculino, Femenino, Unisex
- Tipo de Fragancia: Floral, Oriental, Amaderado, Fresco, Cítrico, Frutal, Especiado, Acuático, Gourmand
- Volumen en mililitros

**Control Financiero:**
- Precio de venta al público
- Costo de adquisición
- Cálculo automático de margen de ganancia (%)
- Proveedor

**Control de Inventario:**
- Cantidad actual en stock
- Stock mínimo (punto de reorden)
- Alertas visuales cuando stock <= stock mínimo

**Identificación:**
- SKU único (código interno)
- Código de barras
- Imagen del producto

**Metadatos del Sistema:**
- Fecha de creación
- Fecha de última actualización
- Usuario que creó/modificó el registro

### 2.2 Sistema de Búsqueda y Filtrado

El personal debe poder localizar productos rápidamente mediante:

**Búsqueda Textual:**
- Por nombre de producto
- Por marca
- Por SKU
- Por código de barras

**Filtros Combinables:**
- Por categoría de producto
- Por género
- Por tipo de fragancia
- Por rango de precios (mínimo y máximo)
- Por nivel de stock
- Productos con stock bajo (alerta)

**Ordenamiento:**
- Por fecha de creación (más recientes primero)
- Por nombre alfabético
- Por marca
- Por precio (ascendente/descendente)
- Por cantidad en stock

### 2.3 Sistema de Auditoría y Trazabilidad

**Registro Automático de Operaciones:**
- Todas las operaciones CRUD (Crear, Leer, Actualizar, Eliminar) deben quedar registradas
- Información a registrar:
  - Usuario que realizó la acción
  - Producto afectado (ID y nombre)
  - Tipo de acción (Creación, Edición, Eliminación)
  - Cambios específicos (valores anteriores y nuevos)
  - Fecha y hora exacta

**Consulta de Historial:**
- Los administradores pueden ver historial completo de todos los usuarios
- Los vendedores solo pueden ver su propio historial
- Filtros por usuario, producto y tipo de acción
- Vista detallada de cada cambio realizado

### 2.4 Sistema de Usuarios y Roles

**Roles Definidos:**

1. **Administrador:**
   - Gestión completa de productos (crear, editar, eliminar)
   - Creación y eliminación de usuarios
   - Asignación de roles (Administrador/Vendedor)
   - Acceso completo al historial de todos los usuarios
   - Visualización de todas las ventas
   - Acceso a reportes y análisis

2. **Vendedor:**
   - Gestión completa de productos (crear, editar, eliminar)
   - Registro de ventas
   - Acceso solo a su propio historial
   - Visualización de sus propias ventas
   - Consulta de inventario

**Seguridad:**
- Autenticación obligatoria para acceder al sistema
- Sesiones con timeout automático
- Prevención de auto-eliminación de usuarios
- Validación de permisos en cada operación

### 2.5 Sistema de Punto de Venta

**Carrito de Compras:**
- Agregar productos al carrito desde el catálogo
- Visualizar productos en el carrito
- Modificar cantidades
- Eliminar productos del carrito
- Cálculo automático de subtotales y total
- Validación de stock disponible

**Proceso de Venta:**
- Generación automática de número de ticket
- Registro de vendedor que realizó la venta
- Descuento automático de inventario
- Almacenamiento de items vendidos con:
  - Nombre del producto
  - Marca
  - SKU
  - Cantidad vendida
  - Precio unitario al momento de la venta
  - Subtotal
- Fecha y hora de la venta

**Ticket de Venta:**
- Generación automática de ticket digital
- Información incluida:
  - Logo y datos de Rubi perfumeria
  - Número de ticket único
  - Fecha y hora
  - Vendedor que atendió
  - Lista detallada de productos
  - Cantidades y precios
  - Subtotales
  - Total de la venta
  - Total de artículos
- Opción de impresión
- Diseño elegante acorde a la imagen de la perfumería

**Consulta de Ventas:**
- Lista completa de ventas realizadas
- Administradores ven todas las ventas
- Vendedores ven solo sus ventas
- Filtro por vendedor (solo administradores)
- Vista detallada de cada venta
- Información de productos vendidos

---

## 3. Requerimientos No Funcionales

### 3.1 Diseño e Interfaz de Usuario

**Identidad Visual:**
- Paleta de colores acorde a marca Rubi perfumeria:
  - Cream (#FAF7F2) - Color de fondo principal
  - Beige (#E8DCC4) - Bordes y detalles
  - Dark Brown (#5C4A3A) - Textos principales
  - Gold Accent (#C9A961) - Acentos y elementos destacados
  - Soft Brown (#8B7355) - Botones y elementos interactivos

**Tipografía:**
- Cormorant Garamond (serif) para títulos - peso 600
- Inter (sans-serif) para texto - peso 500-600
- Espaciado de letras optimizado para legibilidad

**Elementos de Diseño:**
- Cards minimalistas con bordes sutiles
- Animaciones suaves en hover
- Indicadores visuales de estado
- Iconos SVG para mejor experiencia
- Diseño responsive (adaptable a tablets y móviles)
- Sistema de notificaciones elegante

### 3.2 Rendimiento

- Carga de página inicial < 2 segundos
- Búsquedas y filtros con respuesta inmediata
- Optimización de imágenes de productos
- Paginación en listados extensos
- Carga diferida de imágenes (lazy loading)

### 3.3 Usabilidad

- Interfaz intuitiva sin necesidad de capacitación extensa
- Formularios con validación en tiempo real
- Mensajes de error claros y accionables
- Confirmación antes de acciones destructivas
- Breadcrumbs para navegación clara
- Shortcuts de teclado para operaciones frecuentes

### 3.4 Compatibilidad

- Navegadores modernos (Chrome, Firefox, Safari, Edge)
- Responsive design para tablets
- Soporte para impresión de tickets
- Compatible con lectores de código de barras (input estándar)

---

## 4. Especificaciones Técnicas

### 4.1 Arquitectura del Sistema

**Patrón de Diseño:** MVC (Model-View-Controller) mediante Django

**Stack Tecnológico:**
- **Backend Framework:** Django 5.2.8
- **Lenguaje:** Python 3.12
- **Base de Datos:** SQLite3 (con posibilidad de migrar a PostgreSQL)
- **Frontend:** HTML5, CSS3, JavaScript
- **Framework CSS:** TailwindCSS 3.x (vía CDN)
- **Procesamiento de Imágenes:** Pillow 12.0.0
- **Servidor Web Desarrollo:** Django Development Server
- **Servidor Web Producción:** Compatible con Gunicorn/uWSGI

### 4.2 Estructura de la Base de Datos

#### Modelo: Product (Producto)
```
Campos:
- id (PK, AutoField)
- name (CharField, 200)
- brand (CharField, 100)
- description (TextField)
- category (CharField, 20, choices)
- gender (CharField, 1, choices)
- fragrance_type (CharField, 20, choices, optional)
- volume (Integer)
- price (DecimalField, 10, 2)
- cost (DecimalField, 10, 2)
- quantity (Integer)
- min_stock (Integer, default=5)
- sku (CharField, 100, unique)
- barcode (CharField, 50, optional)
- supplier (CharField, 200, optional)
- image (ImageField, optional)
- created_at (DateTimeField, auto_now_add)
- updated_at (DateTimeField, auto_now)

Propiedades Calculadas:
- is_low_stock (Boolean)
- profit_margin (Decimal)

Índices:
- sku (unique)
- name, brand (para búsquedas)
```

#### Modelo: History (Historial)
```
Campos:
- id (PK, AutoField)
- user (ForeignKey -> User, CASCADE)
- product_id (Integer)
- product_name (CharField, 200)
- action (CharField, 10, choices: CREATE/UPDATE/DELETE)
- changes (TextField, JSON)
- timestamp (DateTimeField, auto_now_add)

Índices:
- user, timestamp (para consultas)
- product_id (para trazabilidad)
```

#### Modelo: UserProfile (Perfil de Usuario)
```
Campos:
- id (PK, AutoField)
- user (OneToOneField -> User, CASCADE)
- is_admin (BooleanField, default=False)
- role (CharField, 10, choices: SELLER/ADMIN, default=SELLER)

Relaciones:
- Signal post_save para creación automática
```

#### Modelo: Sale (Venta)
```
Campos:
- id (PK, AutoField)
- user (ForeignKey -> User, CASCADE) [vendedor]
- total (DecimalField, 10, 2)
- created_at (DateTimeField, auto_now_add)
- ticket_number (CharField, 50, unique)

Métodos:
- get_items_count() -> Integer
```

#### Modelo: SaleItem (Item de Venta)
```
Campos:
- id (PK, AutoField)
- sale (ForeignKey -> Sale, CASCADE)
- product_name (CharField, 200)
- product_brand (CharField, 100)
- product_sku (CharField, 100)
- quantity (Integer)
- unit_price (DecimalField, 10, 2)
- subtotal (DecimalField, 10, 2)
```

### 4.3 Rutas del Sistema

**Autenticación:**
- `GET /login/` - Página de inicio de sesión
- `POST /login/` - Procesamiento de login
- `GET /logout/` - Cerrar sesión

**Productos:**
- `GET /` - Redirige a lista de productos
- `GET /products/` - Lista de productos (con filtros y búsqueda)
- `GET /products/create/` - Formulario de creación
- `POST /products/create/` - Procesar creación
- `GET /products/<id>/` - Detalle de producto
- `GET /products/<id>/edit/` - Formulario de edición
- `POST /products/<id>/edit/` - Procesar edición
- `GET /products/<id>/delete/` - Confirmación de eliminación
- `POST /products/<id>/delete/` - Procesar eliminación

**Carrito y Ventas:**
- `POST /cart/add/<product_id>/` - Agregar producto al carrito
- `GET /cart/` - Ver carrito de compras
- `POST /cart/update/<product_id>/` - Actualizar cantidad
- `POST /cart/remove/<product_id>/` - Eliminar del carrito
- `POST /cart/checkout/` - Procesar venta
- `GET /sales/` - Lista de ventas
- `GET /sales/<id>/` - Detalle de venta
- `GET /sales/<id>/ticket/` - Ticket de venta (imprimible)

**Historial:**
- `GET /history/` - Lista de historial (con filtros)
- `GET /history/<id>/` - Detalle de cambio

**Usuarios (Solo Admin):**
- `GET /users/` - Lista de usuarios
- `GET /users/create/` - Formulario de creación
- `POST /users/create/` - Procesar creación
- `POST /users/<id>/delete/` - Eliminar usuario

**Administración Django:**
- `GET /admin/` - Panel de administración

### 4.4 Seguridad Implementada

**Autenticación y Autorización:**
- Decorador `@login_required` en todas las vistas
- Verificación de permisos según rol
- Sesiones seguras con Django
- Protección CSRF en formularios
- Validación de permisos en backend

**Validaciones:**
- Unicidad de SKU
- Validación de stock antes de ventas
- Prevención de eliminación del propio usuario
- Sanitización de inputs
- Validación de tipos de datos
- Verificación de existencia de registros

**Auditoría:**
- Log de todas las operaciones CRUD
- Registro de cambios con detalle
- Trazabilidad por usuario
- Timestamps automáticos

---

## 5. Funcionalidades Implementadas

### 5.1 Módulo de Productos

✅ **Catálogo Completo:**
- 52 perfumes precargados de marcas premium
- Información completa de cada producto
- Imágenes personalizadas para cada perfume
- Categorización por género, tipo de fragancia y categoría

✅ **Operaciones CRUD:**
- Crear nuevos productos con formulario organizado en secciones
- Editar productos existentes con prellenado de datos
- Eliminar productos con confirmación
- Visualización detallada con diseño premium

✅ **Búsqueda Avanzada:**
- Búsqueda en tiempo real por múltiples campos
- Filtros combinables (categoría, género, fragancia, precio)
- Ordenamiento flexible
- Filtro especial para stock bajo

✅ **Control de Inventario:**
- Alertas visuales de stock bajo
- Cálculo automático de margen de ganancia
- Indicadores de cantidad disponible
- Actualización automática al realizar ventas

### 5.2 Módulo de Ventas

✅ **Sistema de Carrito:**
- Agregar productos desde catálogo con un clic
- Vista del carrito con totales calculados
- Modificación de cantidades
- Eliminación de productos
- Validación de stock en tiempo real

✅ **Proceso de Venta:**
- Generación automática de ticket único
- Registro del vendedor
- Descuento automático de inventario
- Almacenamiento de venta completa
- Confirmación visual de venta exitosa

✅ **Tickets Digitales:**
- Diseño elegante acorde a Rubi perfumeria
- Logo y datos del negocio
- Información completa de la venta
- Detalle de cada producto
- Totales y subtotales
- Función de impresión optimizada

✅ **Consulta de Ventas:**
- Lista de todas las ventas realizadas
- Filtro por vendedor (administradores)
- Vista detallada de cada venta
- Información de productos vendidos
- Fecha, hora y vendedor

### 5.3 Módulo de Auditoría

✅ **Historial Completo:**
- Registro automático de todas las operaciones
- Vista cronológica de cambios
- Detalle exacto de modificaciones (antes/después)
- Filtros por usuario, producto y acción

✅ **Trazabilidad:**
- Identificación del responsable de cada cambio
- Timestamps precisos
- Información del producto afectado
- Tipo de operación realizada

### 5.4 Módulo de Administración

✅ **Gestión de Usuarios:**
- Creación de nuevos usuarios (vendedores/administradores)
- Asignación de roles
- Eliminación de usuarios
- Lista completa con roles visibles

✅ **Control de Acceso:**
- Permisos diferenciados por rol
- Restricciones según tipo de usuario
- Validación de permisos en cada operación

### 5.5 Interfaz y Experiencia de Usuario

✅ **Diseño Premium:**
- Paleta de colores corporativa de Rubi perfumeria
- Tipografía elegante y legible
- Animaciones suaves
- Cards minimalistas
- Gradientes y bordes decorativos

✅ **Componentes Visuales:**
- Sistema de notificaciones animado
- Badges y etiquetas coloridas
- Iconos SVG profesionales
- Imágenes de productos optimizadas
- Footer corporativo

✅ **Navegación:**
- Navbar sticky con logo
- Menú principal intuitivo
- Breadcrumbs en vistas detalladas
- Botones de acción claramente identificados
- Carrito visible con contador

✅ **Formularios:**
- Organización en secciones lógicas
- Validación en tiempo real
- Mensajes de error claros
- Prellenado de datos en edición
- Dropdowns con opciones predefinidas

---

## 6. Instalación y Despliegue

### 6.1 Requisitos del Sistema

**Software Requerido:**
- Python 3.12 o superior
- pip (gestor de paquetes)
- Git (opcional, para clonar repositorio)

**Hardware Mínimo:**
- 2 GB RAM
- 500 MB espacio en disco
- Procesador 1.5 GHz

### 6.2 Instalación

**1. Obtener el Código:**
```bash
git clone [repositorio]
cd DjangoCrud
```

**2. Crear Entorno Virtual:**
```bash
python -m venv venv
```

**3. Activar Entorno Virtual:**
```bash
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

**4. Instalar Dependencias:**
```bash
pip install -r requirements.txt
```

**5. Configurar Base de Datos:**
```bash
python manage.py migrate
```

**6. Crear Usuario Administrador:**
```bash
python manage.py shell
```
```python
from django.contrib.auth.models import User
from products.models import UserProfile

admin = User.objects.create_user(
    username='admin',
    password='admin123',
    email='admin@rubiperfumeria.com'
)
admin.profile.role = 'ADMIN'
admin.profile.is_admin = True
admin.profile.save()
```

**7. Iniciar Servidor:**
```bash
python manage.py runserver
```

**8. Acceder al Sistema:**
```
URL: http://127.0.0.1:8000
Usuario: admin
Contraseña: admin123
```

### 6.3 Configuración de Producción

**Variables de Entorno:**
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['rubiperfumeria.com', 'www.rubiperfumeria.com']
SECRET_KEY = 'clave-secreta-generada'
```

**Servidor Web:**
- Recomendado: Gunicorn + Nginx
- Configurar archivos estáticos: `python manage.py collectstatic`
- Configurar archivos media para uploads

**Base de Datos Producción:**
- Migrar a PostgreSQL o MySQL
- Configurar backups automáticos
- Optimizar índices

---

## 7. Usuarios del Sistema

### Credenciales de Acceso

**Usuario Administrador:**
- Usuario: `admin`
- Contraseña: `admin123`
- Rol: Administrador
- Permisos: Completos

**Usuarios Vendedores:**
- Usuario: `usuario`
- Contraseña: `usuario123`
- Rol: Vendedor

- Usuario: `cristian`
- Contraseña: `123456`
- Rol: Vendedor

---

## 8. Inventario Inicial

El sistema incluye un catálogo inicial de **52 perfumes de marcas premium**:

**Marcas Incluidas:**
- Dior (3 productos)
- Chanel (4 productos)
- Yves Saint Laurent (4 productos)
- Paco Rabanne (5 productos)
- Tom Ford (4 productos)
- Giorgio Armani (2 productos)
- Carolina Herrera (3 productos)
- Versace (3 productos)
- Jean Paul Gaultier (4 productos)
- Calvin Klein (2 productos)
- Creed (2 productos)
- Jo Malone (2 productos)
- Maison Francis Kurkdjian (1 producto)
- Y más marcas premium...

Todos los productos incluyen:
- Información completa
- Precios y costos configurados
- Stock inicial
- Imágenes personalizadas
- SKU único
- Clasificación por género y tipo de fragancia

---

## 9. Mantenimiento y Soporte

### Actualizaciones Regulares
- Actualización de dependencias de seguridad
- Optimización de consultas a base de datos
- Mejoras en la interfaz de usuario
- Corrección de bugs reportados

### Backups
- Backup diario automático de base de datos
- Backup semanal de archivos media (imágenes)
- Retención de 30 días

### Monitoreo
- Logs de errores en `logs/error.log`
- Logs de acceso en `logs/access.log`
- Monitoreo de espacio en disco
- Alertas de errores críticos

---

## 10. Información de Contacto

**Desarrollado para:**
Rubi perfumeria
Sistema de Gestión Integral

**Tecnología:**
Django 5.2.8 | Python 3.12 | TailwindCSS

**Fecha de Entrega:**
Diciembre 2025

---

**© 2025 Rubi perfumeria - Sistema de Gestión Premium**
