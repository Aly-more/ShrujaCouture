from django.db import models
from django.utils.text import slugify


# ==========================
# CATEGORY MODEL
# ==========================
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


# ==========================
# COLLECTION MODEL
# ==========================
class Collection(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# ==========================
# PRODUCT LABEL MODEL
# ==========================
class ProductLabel(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# ==========================
# PRODUCT MODEL
# ==========================
class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products"
    )

    collections = models.ManyToManyField(
        Collection,
        blank=True,
        related_name="products"
    )

    labels = models.ManyToManyField(
        ProductLabel,
        blank=True,
        related_name="products"
    )

    name = models.CharField(max_length=200)

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    brand = models.CharField(
        max_length=100,
        default="Shruja Couture"
    )

    description = models.TextField(blank=True)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    # ==========================
    # PRODUCT IMAGES
    # ==========================

    main_image = models.ImageField(
        upload_to="products/",
        help_text="Main image displayed throughout the website."
    )

    hover_image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
        help_text="Optional image displayed when the customer hovers over the product."
    )

    available = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    # ==========================================
    # STOCK PROPERTIES
    # ==========================================

    @property
    def total_stock(self):
        return sum(
            variant.stock
            for variant in self.variants.all()
        )

    @property
    def sold_out(self):
        return self.total_stock == 0

    @property
    def low_stock(self):
        return 0 < self.total_stock <= 3

    @property
    def in_stock(self):
        return self.total_stock > 3

    @property
    def available_sizes(self):
        return self.variants.filter(
            stock__gt=0
        )

    @property
    def has_discount(self):
        return (
            self.discount_price is not None
            and self.discount_price < self.price
        )

    @property
    def display_price(self):
        return (
            self.discount_price
            if self.has_discount
            else self.price
        )

    @property
    def is_new_arrival(self):
        return self.labels.filter(
            name="New Arrival"
        ).exists()

    def __str__(self):
        return self.name


# ==========================
# PRODUCT IMAGE MODEL
# ==========================
class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="products/gallery/"
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"

    def __str__(self):
        return f"{self.product.name} - Gallery"


# ==========================
# PRODUCT VARIANT MODEL
# ==========================
class ProductVariant(models.Model):

    SIZE_CHOICES = [
        ("XS", "XS"),
        ("S", "S"),
        ("M", "M"),
        ("L", "L"),
        ("XL", "XL"),
        ("XXL", "XXL"),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants"
    )

    size = models.CharField(
        max_length=5,
        choices=SIZE_CHOICES
    )

    color = models.CharField(
        max_length=50
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    sku = models.CharField(
        max_length=100,
        unique=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product", "size", "color"],
                name="unique_product_variant"
            )
        ]

    def __str__(self):
        return f"{self.product.name} - {self.size} - {self.color}"

class ContactMessage(models.Model):

    full_name = models.CharField(max_length=150)

    email = models.EmailField()

    subject = models.CharField(max_length=200)

    message = models.TextField()

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        ordering = ["-created_at"]

        verbose_name = "Contact Message"

        verbose_name_plural = "Contact Messages"

    def __str__(self):

        return f"{self.full_name} - {self.subject}"