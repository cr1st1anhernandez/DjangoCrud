# -*- coding: utf-8 -*-
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User
from products.models import UserProfile

print("Creando usuario vendedor...")

if User.objects.filter(username='cristian').exists():
    print("El usuario 'cristian' ya existe")
    user = User.objects.get(username='cristian')
    user.profile.role = 'SELLER'
    user.profile.save()
    print("Rol actualizado a vendedor")
else:
    seller_user = User.objects.create_user(
        username='cristian',
        password='123456',
        email='cristian@example.com'
    )
    seller_user.profile.role = 'SELLER'
    seller_user.profile.is_admin = False
    seller_user.profile.save()
    print("Usuario vendedor creado: cristian / 123456")

print("\nUsuario vendedor creado exitosamente!")
print("\nPuedes iniciar sesión con:")
print("  Vendedor: cristian / 123456")
