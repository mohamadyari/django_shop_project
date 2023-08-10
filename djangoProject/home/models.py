from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
import os
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.forms import ModelForm
from django.db.models import Avg
from django_jalali.db import models as jmodels
from django.db.models.signals import post_save


# Create your models here.


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}-{instance.name}{ext}"
    return f"products/{final_name}"


def upload_gallery_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}-{instance.title}{ext}"
    return f"products/galleries/{final_name}"


class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub')
    sub_cat = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    create = jmodels.jDateTimeField(auto_now_add=True)
    update = jmodels.jDateTimeField(auto_now=True)
    slug = models.SlugField(allow_unicode=True, unique=True, null=True, blank=True)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:category', args=[self.slug, self.id])


class Product(models.Model):
    VARIANT = (
        ('None', 'none'),
        ('Size', 'size'),
        ('Color', 'color'),
        ('Both', 'Both'),
    )
    category = models.ManyToManyField(Category, blank=True, related_name='product_category', )
    name = models.CharField(max_length=200)
    amount = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    change = models.BooleanField(default=False)
    discount = models.PositiveIntegerField(blank=True, null=True)
    total_price = models.PositiveIntegerField()
    information = RichTextUploadingField(blank=True, null=True)
    create = jmodels.jDateTimeField(auto_now_add=True)
    update = jmodels.jDateTimeField(auto_now=True)
    tags = TaggableManager(blank=True)
    available = models.BooleanField(default=True)
    status = models.CharField(null=True, blank=True, max_length=200, choices=VARIANT)
    color = models.ManyToManyField('Color', blank=True)
    size = models.ManyToManyField('Size', blank=True)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    like = models.ManyToManyField(User, blank=True, related_name='product_like')
    total_like = models.IntegerField(default=0)
    dislike = models.ManyToManyField(User, blank=True, related_name='product_dislike')
    total_dislike = models.IntegerField(default=0)
    favourite = models.ManyToManyField(User, blank=True, related_name='fa_user')
    total_favourite = models.IntegerField(default=0)
    sell = models.IntegerField(default=0)
    view = models.ManyToManyField(User, blank=True, null=True, related_name='product_view')
    num_view = models.IntegerField(default=0)

    def average(self):
        data = Comment.objects.filter(is_reply=False, product=self).aggregate(avg=Avg('rate'))
        star = 0
        if data['avg'] is not None:
            star = round(data['avg'], 1)
        return star

    def total_like(self):
        return self.like.count()

    def total_dislike(self):
        return self.dislike.count()

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.discount * self.unit_price) / 100
            return int(self.unit_price - total)
        return self.total_price

    def get_absolute_url(self):
        return reverse('home:detail', args=[self.id])


class Size(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Variants(models.Model):
    name = models.CharField(max_length=100)
    update = jmodels.jDateTimeField(auto_now=True)
    product_variant = models.ForeignKey(Product, on_delete=models.CASCADE)
    size_variant = models.ForeignKey(Size, on_delete=models.CASCADE)
    color_variant = models.ForeignKey(Color, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(blank=True, null=True)
    total_price = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.discount * self.unit_price) / 100
            return int(self.unit_price - total)
        return self.total_price


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()
    rate = models.PositiveIntegerField(default=1)
    create = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='comment_reply')
    is_reply = models.BooleanField(default=False)
    comment_like = models.ManyToManyField(User, blank=True, related_name='com_like')
    total_comment_like = models.PositiveIntegerField(default=0)
    comment_dislike = models.ManyToManyField(User, blank=True, related_name='com_dislike')
    total_comment_dislike = models.PositiveIntegerField(default=0)

    def total_comment_like(self):
        return self.comment_like.count()

    def total_comment_dislike(self):
        return self.comment_dislike.count()

    def __str__(self):
        return self.product.name


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'rate']


class ReplyForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Gallery(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='gallery/', blank=True)

    def __str__(self):
        return self.name


class Chart(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    unit_price = models.IntegerField(default=0)
    update = jmodels.jDateTimeField(auto_now=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, related_name='pr_update')
    variant = models.ForeignKey(Variants, on_delete=models.CASCADE, blank=True, null=True, related_name='v_update')

    def __str__(self):
        return self.name


def product_post_saved(sender, instance, created, *args, **kwargs):
    data = instance
    if data.change == True:
        Chart.objects.create(product=data, unit_price=data.unit_price, update=data.update, name=data.name)


post_save.connect(product_post_saved, sender=Product)


def variant_post_saved(sender, instance, created, *args, **kwargs):
    data = instance

    Chart.objects.create(variant=data, unit_price=data.unit_price, update=data.update, name=data.name,
                         size=data.size_variant, color=data.color_variant)


post_save.connect(variant_post_saved, sender=Variants)


class Views(models.Model):
    ip = models.CharField(max_length=200, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name
