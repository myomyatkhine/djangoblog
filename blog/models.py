from django.db import models
from django.utils.text import slugify
from PIL import Image

class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name


class Tag(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name


class Post(models.Model):

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    cover_image = models.ImageField(
        upload_to="post_covers/",
        blank=True,
        null=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts"
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True
    )

    title = models.CharField(
        max_length=200
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    content = models.TextField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="draft"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

        if self.cover_image:
            img_path = self.cover_image.path
            img = Image.open(img_path)

            if img.height > 800 or img.width > 800:
                img.thumbnail((800, 800))
                img.save(img_path)