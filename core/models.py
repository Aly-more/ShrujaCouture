from django.db import models


class InstagramPost(models.Model):
    image = models.ImageField(upload_to="instagram/")
    instagram_url = models.URLField(blank=True)
    caption = models.CharField(max_length=200, blank=True)

    is_active = models.BooleanField(default=True)

    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order", "-created_at"]

    def __str__(self):
        return self.caption if self.caption else f"Instagram Post {self.id}"