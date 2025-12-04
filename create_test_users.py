# -*- coding: utf-8 -*-
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User
from products.models import UserProfile

print("Creando usuarios de prueba...")

if User.objects.filter(username='admin').exists():
    print("El usuario 'admin' ya existe")
else:
    admin_user = User.objects.create_user(
        username='admin',
        password='admin123',
        email='admin@example.com'
    )
    admin_user.profile.is_admin = True
    admin_user.profile.save()
    print("Usuario administrador creado: admin / admin123")

if User.objects.filter(username='usuario').exists():
    print("El usuario 'usuario' ya existe")
else:
    normal_user = User.objects.create_user(
        username='usuario',
        password='usuario123',
        email='usuario@example.com'
    )
    normal_user.profile.is_admin = False
    normal_user.profile.save()
    print("Usuario normal creado: usuario / usuario123")

print("\nUsuarios creados exitosamente!")
print("\nPuedes iniciar sesi�n con:")
print("  Administrador: admin / admin123")
print("  Usuario normal: usuario / usuario123")
