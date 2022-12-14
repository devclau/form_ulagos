from django.db import models


class T_UGC_ACTUALIZA_ANTECEDENTES(models.Model):
    RUT = models.CharField(max_length=20)
    TELEFONO1 = models.CharField(max_length=20)
    TELEFONO2 = models.CharField(max_length=20)
    DIRECCION = models.CharField(max_length=200)
    DIRECCION_NUMERO= models.CharField(max_length=10)
    COD_REGION = models.CharField(max_length=10)
    COD_COMUNA = models.CharField(max_length=10)
    CORREO_PARTICULAR=models.CharField(max_length=200)
    FECHA_REGISTRO = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = '"DELFOS"."T$UGC_ACTUALIZA_ANTECEDENTES"'
        verbose_name = 'T$UGC_ACTUALIZA_ANTECEDENTES'
        verbose_name_plural ='T$UGC_ACTUALIZA_ANTECEDENTES'