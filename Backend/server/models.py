from typing import Any
from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from .validators import validate_icon_image_size, validate_image_file_extension


def server_icon_upload_path(instance, filename):
    # Generate the file path for uploading server icons
    # The path includes the server ID and filename to ensure unique storage
    return f"server/{instance.id}/server_icons/{filename}"


def server_banner_upload_path(instance, filename):
    # Generate the file path for uploading server banners
    # The path includes the server ID and filename to ensure unique storage
    return f"server/{instance.id}/server_banners/{filename}"


def category_icon_upload_path(instance, filename):
    # Generate the file path for uploading category icons
    # The path includes the category ID and filename to ensure unique storage
    return f"category/{instance.id}/category_icon/{filename}"


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    desc = models.TextField(blank=True, null=True)
    icon = models.FileField(
        upload_to=category_icon_upload_path,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        """
        Override save method to handle icon replacement.
        """
        if self.id:
            # Check if an existing category with the same ID has a different icon
            existing = get_object_or_404(Category, id=self.id)
            if existing.icon != self.icon:
                # If the icon has changed, delete the old icon file
                existing.icon.delete(save=False)
        # Call the parent class's save method to save the category
        super(Category, self).save(*args, **kwargs)

    @receiver(models.signals.pre_delete, sender="server.Category")
    def category_delete_files(sender, instance, **kwargs):
        """
        Delete icon file when a category is deleted.
        """
        # Iterate over all fields in the category model
        for field in instance._meta.fields:
            if field.name == "icon":
                # Get the icon file associated with this category
                file = getattr(instance, field.name)
                if file:
                    # Delete the file from storage
                    file.delete(save=False)

    def __str__(self):
        return self.name


class Server(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="server_owner"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="server_category"
    )
    desc = models.CharField(max_length=300, blank=True, null=True)
    member = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return f"{self.name}-{self.id}"


class Channel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="channel_owner"
    )
    topic = models.CharField(max_length=100)
    server = models.ForeignKey(
        Server, on_delete=models.CASCADE, related_name="channel_server"
    )
    banner = models.ImageField(
        upload_to=server_banner_upload_path,
        null=True,
        blank=True,
        validators=[validate_image_file_extension],
    )
    icon = models.ImageField(
        upload_to=server_icon_upload_path,
        null=True,
        blank=True,
        validators=[validate_icon_image_size, validate_image_file_extension],
    )

    def save(self, *args, **kwargs):
        """
        Override save method to handle icon replacement.
        """
        if self.id:
            # Check if an existing category with the same ID has a different icon
            existing = get_object_or_404(Channel, id=self.id)
            if existing.icon != self.icon:
                # If the icon has changed, delete the old icon file
                existing.icon.delete(save=False)

            if existing.banner != self.banner:
                # If the banner has changed, delete the old banner file
                existing.banner.delete(save=False)
        # Call the parent class's save method to save the category
        super(Channel, self).save(*args, **kwargs)

    @receiver(models.signals.pre_delete, sender="server.Server")
    def channel_delete_files(sender, instance, **kwargs):
        """
        Delete icon file when a category is deleted.
        """
        # Iterate over all fields in the category model
        for field in instance._meta.fields:
            if field.name == "icon" or field.name == "banner":
                # Get the icon file associated with this category
                file = getattr(instance, field.name)
                if file:
                    # Delete the file from storage
                    file.delete(save=False)

    def __str__(self):
        return self.name
