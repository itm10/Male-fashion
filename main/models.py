from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50)
    product_id = models.ForeignKey('main.Product', on_delete=models.CASCADE)


class Product(models.Model):
    product_name = models.CharField(max_length=150, verbose_name=_('name'))
    description = models.TextField(blank=True, null=True, verbose_name=_('description'))
    price = models.FloatField(verbose_name=_('price'))
    brand = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('brand'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class Shoppingcart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('product name'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    count = models.PositiveIntegerField(default=1, verbose_name=_('count'))
    updateded_time = models.DateTimeField(auto_now_add=True, verbose_name=_('updated_time'))

    class Meta:
        verbose_name = _('Shoppingcart')
        verbose_name_plural = _('Shoppingcarts')


class Order(models.Model):
    STATUS = (
        (1, 'Created'),
        (2, 'Wait for payment'),
        (3, 'Paid'),
        (4, 'Delivering'),
        (5, 'Completed')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS)

    def __str__(self):
        return f'{self.service.product_name} >>>> {self.status}'


class Images(models.Model):
    image = models.ImageField(upload_to='pics')
    service = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'


class Commment(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    profession=models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
