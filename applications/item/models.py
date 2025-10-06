from tortoise import fields, models
from tortoise.expressions import Q
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel


# ---------- CATEGORY ----------
class Category(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    description = fields.CharField(max_length=255, null=True)
    image = fields.CharField(max_length=500)  # store image path/url
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "categories"

    def __str__(self):
        return self.name


# ---------- SUB CATEGORY ----------
class SubCategory(models.Model):
    id = fields.IntField(pk=True)
    category = fields.ForeignKeyField("models.Category", related_name="subcategories", on_delete=fields.CASCADE)
    name = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    banner = fields.CharField(max_length=500)  # path/url
    image = fields.CharField(max_length=500)   # path/url
    popular = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "sub_categories"

    def __str__(self):
        return self.name


# ---------- BANNER ----------
BANNER_OPTION = [
    ("top_banner", "Top Banner"),
    ("bottom_banner", "Bottom Banner"),
    ("new_arrival", "New Arrival Banner"),
    ("hot_deals", "Hot Deals Banner"),
    ("popular_products", "Popular Products Banner"),
]

class Banner(models.Model):
    id = fields.IntField(pk=True)
    banner = fields.CharField(max_length=500)  # path/url
    position = fields.CharField(max_length=20, default="top_banner")
    link = fields.CharField(max_length=2000, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "banners"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.position} - {self.id}. Link: {self.link}"


# ---------- PRODUCT ----------
class Product(models.Model):
    id = fields.IntField(pk=True)
    slug = fields.CharField(max_length=60, unique=True, null=True)
    subcategory = fields.ForeignKeyField("models.SubCategory", related_name="products", on_delete=fields.CASCADE)
    name = fields.CharField(max_length=255)
    video_id = fields.CharField(max_length=400, null=True)
    details = fields.TextField(null=True)
    description = fields.TextField(null=True)
    stock = fields.IntField(default=0)
    price = fields.IntField()
    discount = fields.DecimalField(max_digits=2, decimal_places=0)
    box_price = fields.IntField(default=0)

    weight = fields.DecimalField(max_digits=10, decimal_places=2)

    ratings = fields.FloatField(default=0)

    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    popular = fields.BooleanField(default=False)
    free_delivery = fields.BooleanField(default=False)
    hot_deals = fields.BooleanField(default=False)
    flash_sale = fields.BooleanField(default=False)
    tag = fields.CharField(max_length=2000, null=True, default="ladz")

    class Meta:
        table = "products"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


    
    @property
    def new_arrival(self):
        return datetime.now(timezone.utc) - self.created_at <= timedelta(days=3)

    @property
    def todays_deals(self):
        return self.hot_deals and self.created_at.date() == datetime.now(timezone.utc).date()

    @property
    def discount_price(self):
        return int((self.price * self.discount) / 100)

    @property
    def sell_price(self):
        return self.price - self.discount_price
    
    async def save(self, *args, **kwargs):
        from app.utils import generate_unique
        if not self.slug:
            self.slug = await generate_unique(self.name or "ladz", Product, field="slug")
        await super().save(*args, **kwargs)


# ---------- PRODUCT IMAGE ----------
COLOR_CHOICES = [
    ("#000000", "Black"),
    ("#FFFFFF", "White"),
    ("#FF0000", "Red"),
    ("#00FF00", "Lime"),
    ("#0000FF", "Blue"),
    ("#FFFF00", "Yellow"),
    ("#FFA500", "Orange"),
    ("#800080", "Purple"),
    ("#FFC0CB", "Pink"),
    ("#A52A2A", "Brown"),
    ("#808080", "Gray"),
    ("#00FFFF", "Cyan"),
    ("#008080", "Teal"),
    ("#000080", "Navy"),
    ("#FFD700", "Gold"),
    ("#808000", "Olive"),
    ("#F0E68C", "Khaki"),
    ("#4B0082", "Indigo"),
    ("#E6E6FA", "Lavender"),
    ("#D3D3D3", "Light Gray"),
]

SIZE_CHOICES = [
    ("XS", "Extra Small"),
    ("S", "Small"),
    ("M", "Medium"),
    ("L", "Large"),
    ("XL", "Extra Large"),
    ("XXL", "2X Large"),
    ("3XL", "3X Large"),
]



class ProductImage(models.Model):
    id = fields.IntField(pk=True)
    product = fields.ForeignKeyField("models.Product", related_name="images", on_delete=fields.CASCADE)
    color = fields.CharField(max_length=7, null=True)
    size = fields.CharField(max_length=7, null=True)
    image = fields.CharField(max_length=500)  # path/url
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "product_images"
        ordering = ["created_at"]
