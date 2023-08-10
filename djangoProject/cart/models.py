from django.db import models
from home.models import *
from django.forms import ModelForm


# Create your models here.


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variants, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class CartForm(ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']


class Compare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,)
    session_key = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.product.name


class CompareForm(ModelForm):
    class Meta:
        model = Compare
        fields = ['product']
