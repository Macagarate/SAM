from django.db import models
from usuarios.models import Actividad

class Preferencia(models.Model):
    pref_from = models.ForeignKey(Actividad,related_name='alumno_act_pref_from',on_delete=models.PROTECT)
    pref_to  = models.ForeignKey(Actividad,related_name='alumno_act_to',on_delete=models.PROTECT)
    pref_order = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s prefiere %s - preferecia %s" % (self.pref_from,self.pref_to,self.pref_order)

    class Meta:
        ordering=['id','pref_order']


