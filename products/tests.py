from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from datetime import datetime, timedelta
from .models import Product, History, UserProfile, Sale, SaleItem


class ProductModelTest(TestCase):
    """Tests para el modelo Product"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.product = Product.objects.create(
            name='Test Perfume',
            brand='Test Brand',
            description='Test Description',
            category='PERFUME',
            gender='U',
            fragrance_type='FLORAL',
            volume=100,
            price=Decimal('99.99'),
            cost=Decimal('50.00'),
            quantity=10,
            min_stock=5,
            sku='TEST-001',
            barcode='1234567890',
            supplier='Test Supplier'
        )

    def test_product_creation(self):
        """Test que el producto se crea correctamente"""
        self.assertEqual(self.product.name, 'Test Perfume')
        self.assertEqual(self.product.brand, 'Test Brand')
        self.assertEqual(self.product.price, Decimal('99.99'))
        self.assertEqual(self.product.quantity, 10)

    def test_product_str_method(self):
        """Test del método __str__"""
        expected = f"{self.product.name} - {self.product.brand} ({self.product.volume}ml)"
        self.assertEqual(str(self.product), expected)

    def test_is_low_stock_property(self):
        """Test de la propiedad is_low_stock"""
        # Stock normal
        self.assertFalse(self.product.is_low_stock)

        # Stock bajo
        self.product.quantity = 5
        self.product.save()
        self.assertTrue(self.product.is_low_stock)

        # Stock muy bajo
        self.product.quantity = 2
        self.product.save()
        self.assertTrue(self.product.is_low_stock)

    def test_profit_margin_property(self):
        """Test del cálculo de margen de ganancia"""
        # Margen normal
        expected_margin = ((Decimal('99.99') - Decimal('50.00')) / Decimal('50.00')) * 100
        self.assertAlmostEqual(float(self.product.profit_margin), float(expected_margin), places=2)

        # Sin costo
        self.product.cost = Decimal('0')
        self.product.save()
        self.assertEqual(self.product.profit_margin, 0)

    def test_product_with_image(self):
        """Test de producto con imagen"""
        product_with_image = Product.objects.create(
            name='Perfume with Image',
            brand='Image Brand',
            description='Test',
            price=Decimal('50.00'),
            quantity=5,
            sku='IMG-001'
        )
        self.assertIsNotNone(product_with_image)


class HistoryModelTest(TestCase):
    """Tests para el modelo History"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.product = Product.objects.create(
            name='Test Product',
            brand='Brand',
            description='Description',
            price=Decimal('50.00'),
            quantity=10,
            sku='HIST-001'
        )

    def test_history_creation(self):
        """Test de creación de historial"""
        history = History.objects.create(
            user=self.user,
            product_id=self.product.id,
            product_name=self.product.name,
            action='CREATE',
            changes={'name': 'Test Product', 'price': '50.00'}
        )
        self.assertEqual(history.action, 'CREATE')
        self.assertEqual(history.user, self.user)
        self.assertEqual(history.product_name, 'Test Product')

    def test_history_str_method(self):
        """Test del método __str__"""
        history = History.objects.create(
            user=self.user,
            product_id=self.product.id,
            product_name=self.product.name,
            action='UPDATE',
            changes={}
        )
        expected = f"{self.user.username} - {history.get_action_display()} - {self.product.name}"
        self.assertEqual(str(history), expected)

    def test_history_ordering(self):
        """Test del ordenamiento por timestamp"""
        import time

        history1 = History.objects.create(
            user=self.user,
            product_id=self.product.id,
            product_name='Product 1',
            action='CREATE',
            changes={}
        )

        time.sleep(0.01)  # Pequeño delay para asegurar timestamps diferentes
        history2 = History.objects.create(
            user=self.user,
            product_id=self.product.id,
            product_name='Product 2',
            action='UPDATE',
            changes={}
        )

        histories = History.objects.all()
        # El más reciente debe ser primero (ordering = ['-timestamp'])
        self.assertEqual(histories[0], history2)


class UserProfileModelTest(TestCase):
    """Tests para el modelo UserProfile"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.admin_user = User.objects.create_user(username='adminuser', password='adminpass123')

    def test_user_profile_creation(self):
        """Test de creación automática de perfil"""
        profile = UserProfile.objects.get(user=self.user)
        self.assertIsNotNone(profile)
        self.assertFalse(profile.is_admin)

    def test_admin_profile(self):
        """Test de perfil de administrador"""
        profile = UserProfile.objects.get(user=self.admin_user)
        profile.is_admin = True
        profile.save()
        self.assertTrue(profile.is_admin)

    def test_profile_str_method(self):
        """Test del método __str__"""
        profile = UserProfile.objects.get(user=self.user)
        expected = f"{self.user.username} - {profile.get_role_display()}"
        self.assertEqual(str(profile), expected)


class SaleModelTest(TestCase):
    """Tests para los modelos Sale y SaleItem"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.product1 = Product.objects.create(
            name='Product 1',
            brand='Brand 1',
            description='Desc 1',
            price=Decimal('50.00'),
            quantity=10,
            sku='SALE-001'
        )
        self.product2 = Product.objects.create(
            name='Product 2',
            brand='Brand 2',
            description='Desc 2',
            price=Decimal('75.00'),
            quantity=5,
            sku='SALE-002'
        )
        self.sale = Sale.objects.create(
            user=self.user,
            total=Decimal('175.00'),
            ticket_number='TICKET-001'
        )

    def test_sale_creation(self):
        """Test de creación de venta"""
        self.assertEqual(self.sale.user, self.user)
        self.assertEqual(self.sale.total, Decimal('175.00'))
        self.assertEqual(self.sale.ticket_number, 'TICKET-001')

    def test_sale_str_method(self):
        """Test del método __str__"""
        expected = f"Venta #{self.sale.ticket_number} - ${self.sale.total}"
        self.assertEqual(str(self.sale), expected)

    def test_sale_item_creation(self):
        """Test de creación de items de venta"""
        item = SaleItem.objects.create(
            sale=self.sale,
            product_name=self.product1.name,
            product_brand=self.product1.brand,
            product_sku=self.product1.sku,
            quantity=2,
            unit_price=self.product1.price,
            subtotal=self.product1.price * 2
        )
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.subtotal, Decimal('100.00'))

    def test_get_items_count(self):
        """Test del método get_items_count"""
        # Contar items totales en cantidad (suma de quantities)
        SaleItem.objects.create(
            sale=self.sale,
            product_name=self.product1.name,
            product_brand=self.product1.brand,
            product_sku=self.product1.sku,
            quantity=2,
            unit_price=self.product1.price,
            subtotal=Decimal('100.00')
        )
        SaleItem.objects.create(
            sale=self.sale,
            product_name=self.product2.name,
            product_brand=self.product2.brand,
            product_sku=self.product2.sku,
            quantity=1,
            unit_price=self.product2.price,
            subtotal=Decimal('75.00')
        )
        # get_items_count suma las cantidades: 2 + 1 = 3
        self.assertEqual(self.sale.get_items_count(), 3)

    def test_sale_ordering(self):
        """Test del ordenamiento de ventas"""
        # Las ventas en setUp: self.sale (TICKET-001) ya existe
        import time

        time.sleep(0.01)  # Pequeño delay para asegurar timestamps diferentes
        sale2 = Sale.objects.create(
            user=self.user,
            total=Decimal('100.00'),
            ticket_number='TICKET-002'
        )

        time.sleep(0.01)  # Pequeño delay
        sale3 = Sale.objects.create(
            user=self.user,
            total=Decimal('200.00'),
            ticket_number='TICKET-003'
        )

        sales = Sale.objects.all()
        # La más reciente debe ser primero (ordering = ['-created_at'])
        self.assertEqual(sales[0], sale3)
        # Verificar que todas las ventas están presentes
        self.assertEqual(sales.count(), 3)


class ProductViewsTest(TestCase):
    """Tests para las vistas de productos"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.admin_user = User.objects.create_user(username='admin', password='adminpass123')
        UserProfile.objects.filter(user=self.admin_user).update(is_admin=True)

        self.product = Product.objects.create(
            name='Test Product',
            brand='Test Brand',
            description='Test Description',
            price=Decimal('99.99'),
            cost=Decimal('50.00'),
            quantity=10,
            sku='TEST-001'
        )

    def test_product_list_requires_login(self):
        """Test que product_list requiere autenticación"""
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_product_list_authenticated(self):
        """Test de acceso a lista de productos autenticado"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

    def test_product_create(self):
        """Test de creación de producto"""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'name': 'New Product',
            'brand': 'New Brand',
            'description': 'New Description',
            'category': 'PERFUME',
            'gender': 'U',
            'fragrance_type': 'FLORAL',
            'volume': 100,
            'price': '149.99',
            'cost': '75.00',
            'quantity': 20,
            'min_stock': 5,
            'sku': 'NEW-001'
        }
        response = self.client.post(reverse('product_create'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Product.objects.filter(sku='NEW-001').exists())

    def test_product_edit(self):
        """Test de edición de producto"""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'name': 'Updated Product',
            'brand': 'Updated Brand',
            'description': 'Updated Description',
            'category': 'PERFUME',
            'gender': 'M',
            'fragrance_type': 'WOODY',
            'volume': 150,
            'price': '129.99',
            'cost': '65.00',
            'quantity': 15,
            'min_stock': 5,
            'sku': 'TEST-001'
        }
        response = self.client.post(reverse('product_edit', args=[self.product.pk]), data)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')

    def test_product_delete(self):
        """Test de eliminación de producto"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('product_delete', args=[self.product.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    def test_product_detail(self):
        """Test de vista de detalle de producto"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('product_detail', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertContains(response, self.product.brand)


class CartViewsTest(TestCase):
    """Tests para las vistas del carrito"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.product = Product.objects.create(
            name='Cart Product',
            brand='Cart Brand',
            description='Cart Description',
            price=Decimal('50.00'),
            quantity=10,
            sku='CART-001'
        )

    def test_cart_add(self):
        """Test de agregar producto al carrito"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('cart_add', args=[self.product.pk]))
        self.assertEqual(response.status_code, 302)

        # Verificar que el carrito tiene el producto
        session = self.client.session
        cart = session.get('cart', {})
        self.assertIn(str(self.product.pk), cart)

    def test_cart_view(self):
        """Test de vista del carrito"""
        self.client.login(username='testuser', password='testpass123')

        # Agregar producto al carrito
        self.client.get(reverse('cart_add', args=[self.product.pk]))

        # Ver carrito
        response = self.client.get(reverse('cart_view'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_cart_update_quantity(self):
        """Test de actualización de cantidad en carrito"""
        self.client.login(username='testuser', password='testpass123')

        # Agregar producto
        self.client.get(reverse('cart_add', args=[self.product.pk]))

        # Actualizar cantidad
        response = self.client.post(
            reverse('cart_update_quantity', args=[self.product.pk]),
            {'quantity': 3}
        )
        self.assertEqual(response.status_code, 302)

        # Verificar nueva cantidad
        session = self.client.session
        cart = session.get('cart', {})
        self.assertEqual(cart[str(self.product.pk)]['quantity'], 3)

    def test_cart_remove(self):
        """Test de eliminar producto del carrito"""
        self.client.login(username='testuser', password='testpass123')

        # Agregar producto
        self.client.get(reverse('cart_add', args=[self.product.pk]))

        # Remover producto
        response = self.client.get(reverse('cart_remove', args=[self.product.pk]))
        self.assertEqual(response.status_code, 302)

        # Verificar que se eliminó
        session = self.client.session
        cart = session.get('cart', {})
        self.assertNotIn(str(self.product.pk), cart)

    def test_cart_clear(self):
        """Test de limpiar carrito"""
        self.client.login(username='testuser', password='testpass123')

        # Agregar productos
        self.client.get(reverse('cart_add', args=[self.product.pk]))

        # Limpiar carrito
        response = self.client.get(reverse('cart_clear'))
        self.assertEqual(response.status_code, 302)

        # Verificar que está vacío
        session = self.client.session
        cart = session.get('cart', {})
        self.assertEqual(len(cart), 0)


class SaleViewsTest(TestCase):
    """Tests para las vistas de ventas"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.product = Product.objects.create(
            name='Sale Product',
            brand='Sale Brand',
            description='Sale Description',
            price=Decimal('100.00'),
            quantity=10,
            sku='SALE-001'
        )

    def test_sale_process_reduces_stock(self):
        """Test que procesar venta reduce el stock"""
        self.client.login(username='testuser', password='testpass123')

        # Agregar producto al carrito
        self.client.get(reverse('cart_add', args=[self.product.pk]))
        self.client.post(
            reverse('cart_update_quantity', args=[self.product.pk]),
            {'quantity': 2}
        )

        # Procesar venta
        initial_quantity = self.product.quantity
        response = self.client.get(reverse('sale_process'))

        # Verificar reducción de stock
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, initial_quantity - 2)

        # Verificar que se creó la venta
        self.assertTrue(Sale.objects.exists())

    def test_sale_process_insufficient_stock(self):
        """Test que no se puede vender más del stock disponible"""
        self.client.login(username='testuser', password='testpass123')

        # Intentar agregar más cantidad que el stock
        self.product.quantity = 2
        self.product.save()

        self.client.get(reverse('cart_add', args=[self.product.pk]))
        self.client.post(
            reverse('cart_update_quantity', args=[self.product.pk]),
            {'quantity': 5}  # Más que el stock disponible
        )

        response = self.client.get(reverse('sale_process'))
        # Debe redirigir de vuelta al carrito con error
        self.assertEqual(response.status_code, 302)

    def test_sale_list(self):
        """Test de lista de ventas"""
        self.client.login(username='testuser', password='testpass123')

        # Crear una venta
        sale = Sale.objects.create(
            user=self.user,
            total=Decimal('100.00'),
            ticket_number='TEST-TICKET-001'
        )

        response = self.client.get(reverse('sale_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TEST-TICKET-001')

    def test_sale_detail(self):
        """Test de detalle de venta"""
        self.client.login(username='testuser', password='testpass123')

        # Crear venta con items
        sale = Sale.objects.create(
            user=self.user,
            total=Decimal('100.00'),
            ticket_number='TEST-TICKET-002'
        )
        SaleItem.objects.create(
            sale=sale,
            product_name=self.product.name,
            product_brand=self.product.brand,
            product_sku=self.product.sku,
            quantity=1,
            unit_price=self.product.price,
            subtotal=self.product.price
        )

        response = self.client.get(reverse('sale_detail', args=[sale.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_sale_ticket(self):
        """Test de ticket de venta"""
        self.client.login(username='testuser', password='testpass123')

        sale = Sale.objects.create(
            user=self.user,
            total=Decimal('50.00'),
            ticket_number='TEST-TICKET-003'
        )

        response = self.client.get(reverse('sale_ticket', args=[sale.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TEST-TICKET-003')


class HistoryViewsTest(TestCase):
    """Tests para las vistas de historial"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.product = Product.objects.create(
            name='History Product',
            brand='History Brand',
            description='History Description',
            price=Decimal('75.00'),
            quantity=5,
            sku='HIST-001'
        )

    def test_history_list(self):
        """Test de lista de historial"""
        self.client.login(username='testuser', password='testpass123')

        # Crear historial
        history = History.objects.create(
            user=self.user,
            product_id=self.product.id,
            product_name=self.product.name,
            action='CREATE',
            changes={'name': self.product.name}
        )

        response = self.client.get(reverse('history_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_history_detail(self):
        """Test de detalle de historial"""
        self.client.login(username='testuser', password='testpass123')

        history = History.objects.create(
            user=self.user,
            product_id=self.product.id,
            product_name=self.product.name,
            action='UPDATE',
            changes={'price': {'old': '50.00', 'new': '75.00'}}
        )

        response = self.client.get(reverse('history_detail', args=[history.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)


class URLTest(TestCase):
    """Tests para las URLs"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.product = Product.objects.create(
            name='URL Test Product',
            brand='URL Brand',
            description='URL Description',
            price=Decimal('50.00'),
            quantity=10,
            sku='URL-001'
        )
        self.sale = Sale.objects.create(
            user=self.user,
            total=Decimal('50.00'),
            ticket_number='URL-TICKET-001'
        )
        self.history = History.objects.create(
            user=self.user,
            product_id=self.product.id,
            product_name=self.product.name,
            action='CREATE',
            changes={}
        )

    def test_urls_resolve(self):
        """Test que todas las URLs principales resuelven correctamente"""
        self.client.login(username='testuser', password='testpass123')

        urls_to_test = [
            ('product_list', None),
            ('product_create', None),
            ('product_detail', [self.product.pk]),
            ('product_edit', [self.product.pk]),
            ('product_delete', [self.product.pk]),
            ('cart_view', None),
            ('cart_add', [self.product.pk]),
            ('sale_list', None),
            ('sale_detail', [self.sale.pk]),
            ('sale_ticket', [self.sale.pk]),
            ('history_list', None),
            ('history_detail', [self.history.pk]),
        ]

        for url_name, args in urls_to_test:
            if args:
                url = reverse(url_name, args=args)
            else:
                url = reverse(url_name)

            response = self.client.get(url)
            # Verificar que no da error 404
            self.assertNotEqual(response.status_code, 404,
                              f"URL {url_name} returned 404")
