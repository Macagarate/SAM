from django.db import models

# Create your models here.

class Person(models.Model):
    TYPE_STUDENT = [
        ('PR', 'Mechon'),
        ('AH', 'Ahijado'),
    ]
    name =  models.CharField(max_length=200, null=False)
    type_student = models.CharField(max_length=2, choices=TYPE_STUDENT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return "%s - %s" % (self.type_student,self.name)

class Preference(models.Model):
    pref_from = models.ForeignKey(Person,related_name='person_pref_from',on_delete=models.PROTECT)
    pref_to  = models.ForeignKey(Person,related_name='person_pref_to',on_delete=models.PROTECT)
    pref_order = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s prefiere %s - preferecia %s" % (self.pref_from,self.pref_to,self.pref_order)

    class Meta:
        ordering=['id','pref_order']


