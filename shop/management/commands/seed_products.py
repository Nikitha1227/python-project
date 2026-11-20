from decimal import Decimal
from django.core.management.base import BaseCommand
from shop.models import Product


class Command(BaseCommand):
    help = "Seeds all 9 products with images"

    def handle(self, *args, **options):
        samples = [
            {
                "name": "Wireless Mechanical Keyboard",
                "description": "Compact 75% tactile mechanical keyboard with USB-C.",
                "price": Decimal("3499.00"),
                "stock": 5,
                "image_url": "https://images.unsplash.com/photo-1595225476474-87563907a212?w=600&q=80",
            },
            {
                "name": "Ergonomic Laptop Stand",
                "description": "Adjustable aluminum stand for desk setups.",
                "price": Decimal("1299.00"),
                "stock": 8,
                "image_url": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=600&q=80",
            },
            {
                "name": "USB-C Multiport Hub",
                "description": "4K HDMI, 100W PD charging, and 3x USB 3.0 ports.",
                "price": Decimal("1899.00"),
                "stock": 3,
                "image_url": "https://images.unsplash.com/photo-1625842268584-8f3296236761?w=600&q=80",
            },
            {
                "name": "Vertical Ergonomic Mouse",
                "description": "Wireless rechargeable mouse with adjustable DPI.",
                "price": Decimal("1499.00"),
                "stock": 10,
                "image_url": "https://images.unsplash.com/photo-1527814050087-3793815479db?w=600&q=80",
            },
            {
                "name": "27-Inch Monitor Light Bar",
                "description": "Screen-mounted LED task lamp with auto-dimming.",
                "price": Decimal("2499.00"),
                "stock": 4,
                "image_url": "https://images.unsplash.com/photo-1593640408182-31c70c8268f5?w=600&q=80",
            },
            {
                "name": "Braided 100W USB-C Cable",
                "description": "2-meter nylon braided fast-charging data cable.",
                "price": Decimal("499.00"),
                "stock": 15,
                "image_url": "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=600&q=80",
            },
            {
                "name": "Felt Desk Mat",
                "description": "Large 90x40cm wool-felt desk pad with anti-slip base.",
                "price": Decimal("899.00"),
                "stock": 6,
                "image_url": "https://images.unsplash.com/photo-1616400619175-5beda3a17896?w=600&q=80",
            },
            {
                "name": "1080p Autofocus Webcam",
                "description": "Full HD webcam with dual noise-reducing microphones.",
                "price": Decimal("2799.00"),
                "stock": 7,
                "image_url": "https://images.unsplash.com/photo-1587826080692-f439cd0b70da?w=600&q=80",
            },
            {
                "name": "Aluminum Headphone Stand",
                "description": "Weighted desktop headset holder with silicone top pad.",
                "price": Decimal("799.00"),
                "stock": 9,
                "image_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=600&q=80",
            },
        ]

        for item in samples:
            product, created = Product.objects.update_or_create(
                name=item["name"],
                defaults={**item, "is_available": True},
            )
            status = "Created" if created else "Updated"
            self.stdout.write(f"{status}: {product.name}")