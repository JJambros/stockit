from django.test import TestCase
from django.core import mail
from .models import Inventory, SupplierOrder


class SupplierOrderTest(TestCase):
    def test_auto_order_and_notification(self):
        product = Product.objects.create(name="Test Product", stock=10, reorder_level=15, reorder_quantity=20)
        product.stock = 5  # Trigger the reorder signal
        product.save()

        order = SupplierOrder.objects.last()
        self.assertEqual(order.product, product)

        # Check if an email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('New Supplier Order Created', mail.outbox[0].subject)
# Create your tests here.
