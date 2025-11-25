from django.db import models

# Create your models here.


class Produto(models.Model):
    name_product = models.CharField(max_length=200)
    image_product = models.ImageField(upload_to='media/products/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_product