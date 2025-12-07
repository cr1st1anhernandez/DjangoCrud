from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Sum
from django.db import models
from .models import Product, History, UserProfile, Sale, SaleItem
from decimal import Decimal
from datetime import datetime
import json

def user_login(request):
    if request.user.is_authenticated:
        return redirect('product_list')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product_list')
        else:
            messages.error(request, 'Usuario o contrasena incorrectos')

    return render(request, 'products/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def user_list(request):
    if not hasattr(request.user, 'profile') or not request.user.profile.is_admin:
        messages.error(request, 'No tienes permisos para acceder a esta pagina')
        return redirect('product_list')

    users = User.objects.all().select_related('profile')
    return render(request, 'products/user_list.html', {'users': users})

@login_required
def user_create(request):
    if not hasattr(request.user, 'profile') or not request.user.profile.is_admin:
        messages.error(request, 'No tienes permisos para acceder a esta pagina')
        return redirect('product_list')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        is_admin = request.POST.get('is_admin') == 'on'

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe')
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.profile.is_admin = is_admin
            user.profile.save()
            messages.success(request, 'Usuario creado exitosamente')
            return redirect('user_list')

    return render(request, 'products/user_form.html')

@login_required
def user_delete(request, pk):
    if not hasattr(request.user, 'profile') or not request.user.profile.is_admin:
        messages.error(request, 'No tienes permisos para realizar esta accion')
        return redirect('product_list')

    user = get_object_or_404(User, pk=pk)
    if user == request.user:
        messages.error(request, 'No puedes eliminar tu propia cuenta')
        return redirect('user_list')

    user.delete()
    messages.success(request, 'Usuario eliminado exitosamente')
    return redirect('user_list')

@login_required
def product_list(request):
    products = Product.objects.all()

    # Busqueda
    search = request.GET.get('search')
    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(brand__icontains=search) |
            Q(sku__icontains=search) |
            Q(barcode__icontains=search) |
            Q(description__icontains=search)
        )

    # Filtro por categoria
    category = request.GET.get('category')
    if category:
        products = products.filter(category=category)

    # Filtro por genero
    gender = request.GET.get('gender')
    if gender:
        products = products.filter(gender=gender)

    # Filtro por tipo de fragancia
    fragrance = request.GET.get('fragrance')
    if fragrance:
        products = products.filter(fragrance_type=fragrance)

    # Filtro por precio
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)

    # Filtro por cantidad
    quantity_min = request.GET.get('quantity_min')
    if quantity_min:
        products = products.filter(quantity__gte=quantity_min)

    # Filtro de stock bajo
    low_stock = request.GET.get('low_stock')
    if low_stock == 'true':
        from django.db.models import F
        products = products.filter(quantity__lte=F('min_stock'))

    # Ordenamiento
    order_by = request.GET.get('order_by', '-created_at')
    if order_by:
        products = products.order_by(order_by)

    return render(request, 'products/product_list.html', {'products': products})

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

@login_required
def product_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        brand = request.POST.get('brand')
        description = request.POST.get('description')
        category = request.POST.get('category')
        gender = request.POST.get('gender')
        fragrance_type = request.POST.get('fragrance_type')
        volume = request.POST.get('volume')
        price = request.POST.get('price')
        cost = request.POST.get('cost', 0)
        quantity = request.POST.get('quantity')
        min_stock = request.POST.get('min_stock', 5)
        sku = request.POST.get('sku')
        barcode = request.POST.get('barcode', '')
        supplier = request.POST.get('supplier', '')
        expiration_date = request.POST.get('expiration_date')

        product = Product.objects.create(
            name=name,
            brand=brand,
            description=description,
            category=category,
            gender=gender,
            fragrance_type=fragrance_type,
            volume=volume,
            price=price,
            cost=cost,
            quantity=quantity,
            min_stock=min_stock,
            sku=sku,
            barcode=barcode,
            supplier=supplier,
            expiration_date=expiration_date if expiration_date else None
        )

        # Manejo de imagen
        if 'image' in request.FILES:
            product.image = request.FILES['image']
            product.save()

        History.objects.create(
            user=request.user,
            product_id=product.id,
            product_name=product.name,
            action='CREATE',
            changes=json.dumps({
                'name': name,
                'brand': brand,
                'description': description,
                'category': category,
                'gender': gender,
                'fragrance_type': fragrance_type,
                'volume': volume,
                'price': str(price),
                'cost': str(cost),
                'quantity': quantity,
                'min_stock': min_stock,
                'sku': sku,
                'barcode': barcode,
                'supplier': supplier,
                'expiration_date': expiration_date if expiration_date else ''
            })
        )

        messages.success(request, 'Producto creado exitosamente')
        return redirect('product_list')

    return render(request, 'products/product_form.html')

@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        old_data = {
            'name': product.name,
            'brand': product.brand,
            'description': product.description,
            'category': product.category,
            'gender': product.gender,
            'fragrance_type': product.fragrance_type,
            'volume': product.volume,
            'price': str(product.price),
            'cost': str(product.cost),
            'quantity': product.quantity,
            'min_stock': product.min_stock,
            'sku': product.sku,
            'barcode': product.barcode,
            'supplier': product.supplier,
            'expiration_date': str(product.expiration_date) if product.expiration_date else ''
        }

        product.name = request.POST.get('name')
        product.brand = request.POST.get('brand')
        product.description = request.POST.get('description')
        product.category = request.POST.get('category')
        product.gender = request.POST.get('gender')
        product.fragrance_type = request.POST.get('fragrance_type')
        product.volume = request.POST.get('volume')
        product.price = request.POST.get('price')
        product.cost = request.POST.get('cost', 0)
        product.quantity = request.POST.get('quantity')
        product.min_stock = request.POST.get('min_stock', 5)
        product.sku = request.POST.get('sku')
        product.barcode = request.POST.get('barcode', '')
        product.supplier = request.POST.get('supplier', '')
        expiration_date = request.POST.get('expiration_date')
        product.expiration_date = expiration_date if expiration_date else None

        # Manejo de imagen
        if 'image' in request.FILES:
            product.image = request.FILES['image']

        product.save()

        new_data = {
            'name': product.name,
            'brand': product.brand,
            'description': product.description,
            'category': product.category,
            'gender': product.gender,
            'fragrance_type': product.fragrance_type,
            'volume': product.volume,
            'price': str(product.price),
            'cost': str(product.cost),
            'quantity': product.quantity,
            'min_stock': product.min_stock,
            'sku': product.sku,
            'barcode': product.barcode,
            'supplier': product.supplier,
            'expiration_date': str(product.expiration_date) if product.expiration_date else ''
        }

        changes = {}
        for key in old_data:
            if old_data[key] != new_data[key]:
                changes[key] = {'old': old_data[key], 'new': new_data[key]}

        History.objects.create(
            user=request.user,
            product_id=product.id,
            product_name=product.name,
            action='UPDATE',
            changes=json.dumps(changes)
        )

        messages.success(request, 'Producto actualizado exitosamente')
        return redirect('product_list')

    return render(request, 'products/product_form.html', {'product': product})

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        History.objects.create(
            user=request.user,
            product_id=product.id,
            product_name=product.name,
            action='DELETE',
            changes=json.dumps({
                'name': product.name,
                'brand': product.brand,
                'description': product.description,
                'category': product.category,
                'gender': product.gender,
                'fragrance_type': product.fragrance_type,
                'volume': product.volume,
                'price': str(product.price),
                'cost': str(product.cost),
                'quantity': product.quantity,
                'min_stock': product.min_stock,
                'sku': product.sku,
                'barcode': product.barcode,
                'supplier': product.supplier,
                'expiration_date': str(product.expiration_date) if product.expiration_date else ''
            })
        )

        product.delete()
        messages.success(request, 'Producto eliminado exitosamente')
        return redirect('product_list')

    return render(request, 'products/product_confirm_delete.html', {'product': product})

@login_required
def history_list(request):
    histories = History.objects.all()

    is_admin = hasattr(request.user, 'profile') and request.user.profile.is_admin

    if not is_admin:
        histories = histories.filter(user=request.user)

    user_filter = request.GET.get('user')
    product_filter = request.GET.get('product')
    action_filter = request.GET.get('action')

    if user_filter:
        histories = histories.filter(user_id=user_filter)

    if product_filter:
        histories = histories.filter(product_name__icontains=product_filter)

    if action_filter:
        histories = histories.filter(action=action_filter)

    users = User.objects.all() if is_admin else None

    return render(request, 'products/history_list.html', {
        'histories': histories,
        'users': users,
        'is_admin': is_admin,
        'actions': History.ACTION_CHOICES
    })

@login_required
def history_detail(request, pk):
    history = get_object_or_404(History, pk=pk)

    is_admin = hasattr(request.user, 'profile') and request.user.profile.is_admin

    if not is_admin and history.user != request.user:
        messages.error(request, 'No tienes permisos para ver este registro')
        return redirect('history_list')

    changes = history.get_changes_dict()

    return render(request, 'products/history_detail.html', {
        'history': history,
        'changes': changes
    })


# ==================== VISTAS DE CARRITO Y VENTAS ====================

@login_required
def cart_view(request):
    """Vista del carrito de compras"""
    cart = request.session.get('cart', {})
    cart_items = []
    total = Decimal('0.00')

    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            subtotal = Decimal(str(item_data['price'])) * item_data['quantity']
            cart_items.append({
                'product': product,
                'quantity': item_data['quantity'],
                'subtotal': subtotal
            })
            total += subtotal
        except Product.DoesNotExist:
            continue

    return render(request, 'products/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required
def cart_add(request, pk):
    """Agregar producto al carrito"""
    product = get_object_or_404(Product, pk=pk)

    if product.quantity <= 0:
        messages.error(request, f'No hay stock disponible de {product.name}')
        return redirect('product_list')

    cart = request.session.get('cart', {})
    product_id = str(product.id)

    if product_id in cart:
        # Verificar que no exceda el stock disponible
        if cart[product_id]['quantity'] + 1 > product.quantity:
            messages.warning(request, f'No hay suficiente stock de {product.name}. Disponible: {product.quantity}')
            return redirect('cart_view')
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {
            'name': product.name,
            'brand': product.brand,
            'sku': product.sku,
            'price': float(product.price),
            'quantity': 1
        }

    request.session['cart'] = cart
    request.session.modified = True
    messages.success(request, f'{product.name} agregado al carrito')

    return redirect(request.META.get('HTTP_REFERER', 'product_list'))


@login_required
def cart_remove(request, pk):
    """Remover producto del carrito"""
    cart = request.session.get('cart', {})
    product_id = str(pk)

    if product_id in cart:
        product_name = cart[product_id]['name']
        del cart[product_id]
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, f'{product_name} eliminado del carrito')

    return redirect('cart_view')


@login_required
def cart_update_quantity(request, pk):
    """Actualizar cantidad de un producto en el carrito"""
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        cart = request.session.get('cart', {})
        product_id = str(pk)

        try:
            new_quantity = int(request.POST.get('quantity', 1))

            if new_quantity <= 0:
                messages.error(request, 'La cantidad debe ser mayor a 0')
                return redirect('cart_view')

            if new_quantity > product.quantity:
                messages.error(request, f'No hay suficiente stock. Disponible: {product.quantity}')
                return redirect('cart_view')

            if product_id in cart:
                cart[product_id]['quantity'] = new_quantity
                request.session['cart'] = cart
                request.session.modified = True
                messages.success(request, 'Cantidad actualizada')
        except ValueError:
            messages.error(request, 'Cantidad inválida')

    return redirect('cart_view')


@login_required
def cart_clear(request):
    """Limpiar el carrito"""
    request.session['cart'] = {}
    request.session.modified = True
    messages.success(request, 'Carrito vaciado')
    return redirect('cart_view')


@login_required
def sale_process(request):
    """Procesar la venta y generar ticket"""
    cart = request.session.get('cart', {})

    if not cart:
        messages.error(request, 'El carrito está vacío')
        return redirect('cart_view')

    # Verificar stock disponible para todos los productos
    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            if product.quantity < item_data['quantity']:
                messages.error(request, f'Stock insuficiente para {product.name}. Disponible: {product.quantity}')
                return redirect('cart_view')
        except Product.DoesNotExist:
            messages.error(request, f'Producto no encontrado')
            return redirect('cart_view')

    # Crear la venta
    total = Decimal('0.00')
    ticket_number = f"TICKET-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    sale = Sale.objects.create(
        user=request.user,
        total=total,  # Se actualizará después
        ticket_number=ticket_number
    )

    # Crear los items de venta y reducir stock
    for product_id, item_data in cart.items():
        product = Product.objects.get(id=product_id)
        quantity = item_data['quantity']
        unit_price = Decimal(str(item_data['price']))
        subtotal = unit_price * quantity

        # Crear item de venta
        SaleItem.objects.create(
            sale=sale,
            product_name=product.name,
            product_brand=product.brand,
            product_sku=product.sku,
            quantity=quantity,
            unit_price=unit_price,
            subtotal=subtotal
        )

        # Reducir stock
        product.quantity -= quantity
        product.save()

        total += subtotal

    # Actualizar total de la venta
    sale.total = total
    sale.save()

    # Limpiar carrito
    request.session['cart'] = {}
    request.session.modified = True

    messages.success(request, f'Venta realizada exitosamente. Ticket: {ticket_number}')
    return redirect('sale_ticket', pk=sale.id)


@login_required
def sale_ticket(request, pk):
    """Ver el ticket de venta"""
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, 'products/sale_ticket.html', {'sale': sale})


@login_required
def sale_list(request):
    """Lista de todas las ventas"""
    sales = Sale.objects.all()

    is_admin = hasattr(request.user, 'profile') and request.user.profile.is_admin

    # Los usuarios normales solo ven sus propias ventas
    if not is_admin:
        sales = sales.filter(user=request.user)

    # Filtros
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    user_filter = request.GET.get('user')

    if date_from:
        sales = sales.filter(created_at__gte=date_from)
    if date_to:
        sales = sales.filter(created_at__lte=date_to)
    if user_filter and is_admin:
        sales = sales.filter(user_id=user_filter)

    users = User.objects.all() if is_admin else None

    # Calcular totales
    total_sales = sales.aggregate(total=models.Sum('total'))['total'] or 0

    return render(request, 'products/sale_list.html', {
        'sales': sales,
        'users': users,
        'is_admin': is_admin,
        'total_sales': total_sales
    })


@login_required
def sale_detail(request, pk):
    """Detalle de una venta"""
    sale = get_object_or_404(Sale, pk=pk)

    is_admin = hasattr(request.user, 'profile') and request.user.profile.is_admin

    # Verificar permisos
    if not is_admin and sale.user != request.user:
        messages.error(request, 'No tienes permisos para ver esta venta')
        return redirect('sale_list')

    return render(request, 'products/sale_detail.html', {'sale': sale})
