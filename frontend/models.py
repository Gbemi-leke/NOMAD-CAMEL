from django.db import models

from django.db import models
import os


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    main_image = models.ImageField(upload_to="product_images/", blank=True, null=True)  # main image
    hot = models.BooleanField(default=False)
    daily_deal = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        # Delete the main image file if it exists
        if self.main_image and os.path.isfile(self.main_image.path):
            os.remove(self.main_image.path)
        super().delete(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_images/")

    def __str__(self):
        return f"Image for {self.product.name}"

    def delete(self, *args, **kwargs):
        # Delete the gallery image file if it exists
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)
