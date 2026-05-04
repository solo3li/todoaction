from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Product, Cart, CartItem

class StoreModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='buyer', password='password123')
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        self.product = Product.objects.create(
            category=self.category,
            name='Smartphone',
            slug='smartphone',
            price=500.00,
            stock=10
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Smartphone')
        self.assertEqual(self.product.category.name, 'Electronics')

    def test_cart_functionality(self):
        cart = Cart.objects.create(user=self.user)
        item = CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(item.total_price(), 1000.00)
