from django.db import models

# Create your models here.


class NNA(models.Model):
    codNNA = models.CharField(max_length=50, unique=True)
    institucion = models.CharField(max_length=100)
    codProyecto = models.CharField(max_length=50)
    proyecto = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    nombres = models.CharField(max_length=100)
    fechanacimiento = models.DateField()
    rut = models.CharField(max_length=20, unique=True)
    fechaingreso = models.DateField()
    fechaegreso = models.DateField(null=True, blank=True)
    vigencia = models.CharField(max_length=50)
    sexo = models.CharField(max_length=10)
    Nacionalidad = models.CharField(max_length=50)
    TipoAtencion = models.CharField(max_length=100)
    CalidadJuridica = models.CharField(max_length=100)
    DireccionNino = models.CharField(max_length=200)
    RegionNino = models.CharField(max_length=50)
    Comuna = models.CharField(max_length=50)
    SolicitanteIngreso = models.CharField(max_length=100)
    Tribunal = models.CharField(max_length=100)
    Expediente = models.CharField(max_length=100)
    CausalIngreso_1 = models.CharField(max_length=200)

    def __str__(self):
        return self.codNNA
