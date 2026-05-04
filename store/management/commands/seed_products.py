from django.core.management.base import BaseCommand
from store.models import Category, Product

class Command(BaseCommand):
    help = 'Seeds the database with initial products'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Create Categories
        categories_data = [
            {'name': 'Electronics', 'slug': 'electronics'},
            {'name': 'Fashion', 'slug': 'fashion'},
            {'name': 'Home & Garden', 'slug': 'home-garden'},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(**cat_data)
            categories[cat_data['slug']] = category
            if created:
                self.stdout.write(f'Category "{category.name}" created.')

        # Create Products
        products_data = [
            {
                'category': categories['electronics'],
                'name': 'Wireless Headphones',
                'slug': 'wireless-headphones',
                'description': 'High-quality noise-canceling wireless headphones.',
                'price': 199.99,
                'stock': 50,
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80'
            },
            {
                'category': categories['electronics'],
                'name': 'Smart Watch',
                'slug': 'smart-watch',
                'description': 'Elegant smart watch with health tracking features.',
                'price': 249.99,
                'stock': 30,
                'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&q=80'
            },
            {
                'category': categories['fashion'],
                'name': 'Leather Backpack',
                'slug': 'leather-backpack',
                'description': 'Durable and stylish leather backpack for daily use.',
                'price': 89.99,
                'stock': 20,
                'image_url': 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=500&q=80'
            },
            {
                'category': categories['fashion'],
                'name': 'Classic Sunglasses',
                'slug': 'classic-sunglasses',
                'description': 'Timeless design with UV protection.',
                'price': 55.00,
                'stock': 100,
                'image_url': 'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=500&q=80'
            },
            {
                'category': categories['home-garden'],
                'name': 'Ceramic Coffee Mug',
                'slug': 'ceramic-coffee-mug',
                'description': 'Handcrafted ceramic mug for your favorite coffee.',
                'price': 15.99,
                'stock': 200,
                'image_url': 'https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=500&q=80'
            },
            {
                'category': categories['home-garden'],
                'name': 'Indoor Succulent',
                'slug': 'indoor-succulent',
                'description': 'Easy-to-care-for indoor plant in a mini pot.',
                'price': 12.50,
                'stock': 150,
                'image_url': 'https://images.unsplash.com/photo-1520302630591-fd1c66ed11dd?w=500&q=80'
            },
        ]

        for prod_data in products_data:
            product, created = Product.objects.get_or_create(
                slug=prod_data['slug'],
                defaults=prod_data
            )
            if created:
                self.stdout.write(f'Product "{product.name}" created.')
            else:
                self.stdout.write(f'Product "{product.name}" already exists.')

        self.stdout.write(self.style.SUCCESS('Successfully seeded database.'))
