from django.db import models
from usuarios.models import Apadrinamiento

# Create your models here.

class Preferencia(models.Model):
    prefDe = models.ForeignKey(Apadrinamiento,related_name='pref_de',on_delete=models.PROTECT)
    prefHacia  = models.ForeignKey(Apadrinamiento,related_name='pref_hacia',on_delete=models.PROTECT)
    prefOrden = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s prefiere %s - preferecia %s" % (self.prefDe,self.prefHacia,self.prefOrden)

    class Meta:
        ordering=['id','prefOrden']


