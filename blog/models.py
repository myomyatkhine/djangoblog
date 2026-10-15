from django.db import models
from django.conf import settings
from django.utils.text import slugify
from PIL import Image
import uuid


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

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
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
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
        if self.cover_image:
            img_path = self.cover_image.path
            img = Image.open(img_path)
            if img.height > 800 or img.width > 800:
                img.thumbnail((800, 800))
                img.save(img_path)

    def _generate_unique_slug(self):
        # slugify() drops non-ASCII text (e.g. Burmese), so fall back to a
        # short random id when nothing is left.
        base = slugify(self.title) or f"post-{uuid.uuid4().hex[:8]}"
        slug = base
        n = 2

        while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base}-{n}"
            n += 1

        return slug

    def __str__(self):
        return self.title