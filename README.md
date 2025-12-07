# Sistema de Gestión de Perfumería

Sistema completo CRUD para gestión de inventario de perfumería desarrollado con Django, diseñado específicamente para negocios reales de perfumería y cosmética.

## Características Principales

### Gestión Completa de Productos para Perfumería

#### Información Básica
- Nombre del producto
- Marca
- Descripción detallada

#### Categorización Especializada
- **Categorías**: Perfume, Eau de Toilette, Eau de Cologne, Eau de Parfum, Body Spray, Loción Corporal, Crema, Gel, Desodorante
- **Género**: Masculino, Femenino, Unisex
- **Tipos de Fragancia**: Floral, Oriental, Amaderado, Fresco, Cítrico, Frutal, Especiado, Acuático, Gourmand
- **Volumen**: Especificación en mililitros (ml)

#### Control de Inventario y Precios
- Precio de venta al público
- Costo de adquisición
- **Cálculo automático de margen de ganancia**
- Stock actual
- Stock mínimo con **alertas automáticas**
- Notificaciones visuales de productos con stock bajo

#### Identificadores y Trazabilidad
- SKU único
- Código de barras
- Proveedor
- Fecha de vencimiento (opcional)

#### Multimedia
- Carga y visualización de imágenes de productos
- Placeholder automático para productos sin imagen

### Funcionalidades Avanzadas

#### Sistema de Búsqueda y Filtros
- **Búsqueda por texto**: Nombre, marca, SKU, código de barras
- **Filtros múltiples combinables**:
  - Por categoría de producto
  - Por género
  - Por tipo de fragancia
  - Por rango de precios (mínimo y máximo)
  - Por stock mínimo
  - Filtro especial para productos con stock bajo
- **Ordenamiento flexible**: Por fecha, nombre, marca, precio o cantidad en stock

#### Historial de Cambios Completo
- Registro automático de todas las operaciones CRUD
- Información detallada:
  - Usuario que realizó la acción
  - Producto afectado
  - Tipo de acción (Creación, Edición, Eliminación)
  - Detalle exacto de los cambios (antes/después)
  - Fecha y hora precisa
- Sistema de filtros para consultar el historial

#### Sistema de Usuarios y Permisos
**Administrador:**
- Crear y gestionar usuarios
- Acceso completo al historial de todos los usuarios
- Gestión completa de productos

**Usuario Regular:**
- Gestión completa de productos (CRUD)
- Acceso solo a su propio historial

### Interfaz Profesional
- Diseño moderno y responsive con TailwindCSS
- Tarjetas organizadas por categorías de información
- Indicadores visuales de estado (stock bajo, alertas)
- Gradientes y colores temáticos para perfumería
- Iconos SVG para mejor experiencia visual
- Formularios organizados en secciones claras

## Estructura del Proyecto

```
DjangoCrud/
├── media/                  # Archivos multimedia
│   └── products/          # Imágenes de productos
├── mysite/                # Configuración principal
│   ├── settings.py       # Configuración de Django
│   ├── urls.py           # URLs principales
│   └── wsgi.py
├── products/              # Aplicación principal
│   ├── migrations/       # Migraciones de base de datos
│   ├── models.py         # Modelos de datos
│   ├── views.py          # Lógica de vistas
│   ├── urls.py           # URLs de la app
│   └── admin.py          # Configuración del admin
├── templates/             # Templates HTML
│   ├── base.html         # Template base
│   └── products/         # Templates de productos
│       ├── login.html
│       ├── product_list.html
│       ├── product_form.html
│       ├── product_detail.html
│       ├── product_confirm_delete.html
│       ├── history_list.html
│       ├── history_detail.html
│       ├── user_list.html
│       └── user_form.html
├── static/                # Archivos estáticos (CSS/JS)
├── db.sqlite3            # Base de datos SQLite
├── manage.py
├── requirements.txt      # Dependencias del proyecto
├── .gitignore
└── README.md
```

## Modelos de Base de Datos

### Product (Producto)
**Información Básica:**
- name: Nombre del producto
- brand: Marca
- description: Descripción

**Categorización:**
- category: Categoría del producto (choices)
- gender: Género (M/F/U)
- fragrance_type: Tipo de fragancia (choices, opcional)
- volume: Volumen en ml

**Inventario y Precios:**
- price: Precio de venta (decimal)
- cost: Costo de adquisición (decimal)
- quantity: Cantidad en stock (entero)
- min_stock: Stock mínimo (entero)

**Identificadores:**
- sku: Código SKU único
- barcode: Código de barras (opcional)

**Otros:**
- supplier: Proveedor (opcional)
- image: Imagen del producto (ImageField)
- created_at: Fecha de creación
- updated_at: Fecha de última actualización

**Propiedades Calculadas:**
- is_low_stock: Indica si el stock está bajo
- profit_margin: Calcula el margen de ganancia en porcentaje

### History (Historial)
- user: Usuario que realizó la acción
- product_id: ID del producto afectado
- product_name: Nombre del producto
- action: Tipo de acción (CREATE, UPDATE, DELETE)
- changes: Detalles de los cambios en JSON
- timestamp: Fecha y hora de la acción

### UserProfile (Perfil de Usuario)
- user: Relación con User de Django
- is_admin: Booleano que indica si es administrador

## Instalación

### Requisitos Previos
- Python 3.12 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd DjangoCrud
```

2. **Crear entorno virtual**
```bash
python -m venv venv

# Activar en Windows:
venv\Scripts\activate

# Activar en Linux/Mac:
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Aplicar migraciones**
```bash
python manage.py migrate
```

5. **Crear superusuario (opcional)**
```bash
python manage.py createsuperuser
```

6. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

7. **Acceder a la aplicación**
```
http://127.0.0.1:8000
```

## Usuarios de Prueba

Si ya existen usuarios de prueba en la base de datos:

**Administrador:**
- Usuario: `admin`
- Contraseña: `admin123`

**Usuario Normal:**
- Usuario: `usuario`
- Contraseña: `usuario123`

## Uso del Sistema

### Gestión de Productos

#### Crear un Nuevo Producto
1. Click en "Nuevo Producto"
2. Completar el formulario organizado en secciones:
   - **Información Básica**: Nombre, marca, descripción
   - **Categorización**: Categoría, género, tipo de fragancia, volumen
   - **Precios e Inventario**: Costo, precio, stock actual, stock mínimo
   - **Identificadores y Proveedor**: SKU, código de barras, proveedor
   - **Imagen y Vencimiento**: Subir imagen, fecha de vencimiento
3. Click en "Crear Producto"

#### Listar y Filtrar Productos
- Vista en tabla con información clave
- **Búsqueda por texto** en múltiples campos
- **Filtros avanzados** por categoría, género, fragancia
- **Filtros de precio** (rango mínimo-máximo)
- **Filtro de stock bajo** para alertas
- **Ordenamiento** por cualquier columna
- Indicadores visuales:
  - Imágenes en miniatura
  - Badges de categoría
  - Alertas de stock bajo en rojo
  - Margen de ganancia visible

#### Ver Detalle de Producto
Vista completa con diseño profesional mostrando:
- Imagen destacada o placeholder
- Información organizada en tarjetas coloreadas
- Cálculo automático de margen de ganancia
- Alerta visual si el stock está bajo
- Toda la información del producto
- Metadatos del sistema

#### Editar Producto
- Formulario prellenado con datos actuales
- Misma estructura organizada que creación
- Posibilidad de cambiar imagen
- Actualización de stock

#### Eliminar Producto
- Página de confirmación con información del producto
- Registro en historial antes de eliminar

### Historial de Cambios
- Vista completa de todas las operaciones
- Filtros por usuario, producto y tipo de acción
- Detalle completo de cambios (antes/después)
- Diferentes vistas según rol de usuario

### Administración de Usuarios (Solo Admin)
- Crear nuevos usuarios
- Asignar rol de administrador
- Eliminar usuarios
- Lista completa de usuarios del sistema

## Rutas de la Aplicación

- `/` - Redirige a lista de productos
- `/login/` - Página de inicio de sesión
- `/logout/` - Cerrar sesión
- `/products/` - Lista de productos con filtros
- `/products/create/` - Crear nuevo producto
- `/products/<id>/` - Detalle de producto
- `/products/<id>/edit/` - Editar producto
- `/products/<id>/delete/` - Eliminar producto
- `/history/` - Historial de cambios
- `/history/<id>/` - Detalle de un cambio
- `/users/` - Lista de usuarios (solo admin)
- `/users/create/` - Crear usuario (solo admin)
- `/users/<id>/delete/` - Eliminar usuario (solo admin)
- `/admin/` - Panel de administración de Django

## Tecnologías Utilizadas

- **Backend**: Django 5.2.8
- **Base de Datos**: SQLite3
- **Frontend**: HTML5, TailwindCSS (vía CDN)
- **Gestión de Imágenes**: Pillow 12.0.0
- **Python**: 3.12

## Características de Seguridad

- Autenticación requerida en todas las vistas
- Control de permisos basado en roles
- Validación de formularios en servidor
- Protección CSRF en todos los formularios
- Prevención de auto-eliminación de usuarios
- Validación de unicidad en SKU
- Registro de auditoría completo en historial

## Mejoras Futuras Sugeridas

- [ ] Reportes y estadísticas de ventas
- [ ] Exportación a Excel/PDF
- [ ] Sistema de ventas completo
- [ ] Control de clientes
- [ ] Punto de venta (POS)
- [ ] API REST
- [ ] Notificaciones por email para stock bajo
- [ ] Dashboard con gráficas de ventas y stock
- [ ] Generación automática de código de barras
- [ ] Integración con lectores de código de barras
- [ ] Multi-tienda
- [ ] Reportes de productos próximos a vencer
- [ ] Sistema de descuentos y promociones

## Contribuir

Las contribuciones son bienvenidas. Por favor:
1. Fork del proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Soporte

Para reportar problemas o sugerir mejoras, por favor crear un issue en el repositorio.

---

**Sistema de Gestión de Perfumería** - Desarrollado con Django para negocios reales de perfumería y cosmética.
