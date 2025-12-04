from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .models import Product, History, UserProfile
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
            Q(sku__icontains=search) |
            Q(description__icontains=search)
        )

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
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        sku = request.POST.get('sku')

        product = Product.objects.create(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            sku=sku
        )

        History.objects.create(
            user=request.user,
            product_id=product.id,
            product_name=product.name,
            action='CREATE',
            changes=json.dumps({
                'name': name,
                'description': description,
                'price': str(price),
                'quantity': quantity,
                'sku': sku
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
            'description': product.description,
            'price': str(product.price),
            'quantity': product.quantity,
            'sku': product.sku
        }

        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.quantity = request.POST.get('quantity')
        product.sku = request.POST.get('sku')
        product.save()

        new_data = {
            'name': product.name,
            'description': product.description,
            'price': str(product.price),
            'quantity': product.quantity,
            'sku': product.sku
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
                'description': product.description,
                'price': str(product.price),
                'quantity': product.quantity,
                'sku': product.sku
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
