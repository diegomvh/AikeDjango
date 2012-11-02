from django.db import models

# Create your models here.

class Localidad(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Localidades"
        
    def __unicode__(self):
        return u"%s" % self.nombre

class Calle(models.Model):
    """Modelo de calle"""
    nombre = models.CharField(max_length=200)
    nombres = models.TextField(help_text="Otros nombres para esta calle, separados por ;", blank=True)
    localidad = models.ForeignKey(Localidad)
    
    def __unicode__(self):
        return u"%s, %s" % (self.nombre, self.localidad)

class Altura(models.Model):
    """(Altura description)"""
    VEREDA = (
        (1, "par"),
        (2, "impar"),
        (3, "ambas"),
    )
    calle = models.ForeignKey(Calle)
    desde = models.IntegerField()
    hasta = models.IntegerField()
    vereda = models.SmallIntegerField(choices = VEREDA)
    zona = models.PositiveSmallIntegerField(blank=True, null=True)
    barrio = models.CharField(blank=True, max_length=100)

    def __unicode__(self):
        return u"%s, %d - %d" % (self.calle, self.desde, self.hasta)
