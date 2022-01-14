from django.db import models
from cloudinary.models import CloudinaryField
from django.utils.text import slugify


class Personal(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    funcion = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    foto = CloudinaryField("Image", overwrite=True, format="jpg")
    slug = models.SlugField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ("-creado",)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        to_assign = slugify(self.nombre)

        if Personal.objects.filter(slug=to_assign).exists():
            to_assign = to_assign + str(Personal.objects.all().count())

        self.slug = to_assign

        super().save(*args, **kwargs)
