import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from authorization.models import CustomUser
from menu.choices import CATEGORY_CHOICES

User = get_user_model()


def get_product_image_upload_path(instance, filename):
    folder_path = f"ore-restaurant/menu/{instance.menu_item_id}/{timezone.now().strftime('%Y/%m/%d')}/"
    return folder_path + filename


class MenuItemImage(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    menu_item_id = models.ForeignKey(
        'MenuItem', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to=get_product_image_upload_path, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_on']


class MenuItemTag(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    name = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-updated_on']


class MenuItem(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    tags = models.ManyToManyField(MenuItemTag, null=True, default=None)
    is_discounted = models.BooleanField(default=False)
    discount_percentage = models.PositiveIntegerField(
        blank=True, null=True, default=None)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ingredients = models.TextField(blank=True)
    availability = models.BooleanField(default=True)
    nutritionai_information = models.TextField(blank=True)
    preparation_time = models.DurationField(null=True, blank=True)
    spiciness_level = models.CharField(max_length=10, null=True, blank=True)
    availability_schedule = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-updated_on']


class Rating(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True, db_index=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(
        MenuItem, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rating by {self.user.email} for {self.product}: {self.rating}"

    class Meta:
        ordering = ['-updated_on']


class Review(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True, db_index=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(
        MenuItem, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    comment = models.TextField(db_index=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.user.email} for {self.product}: {self.comment}"

    class Meta:
        ordering = ['-updated_on']
