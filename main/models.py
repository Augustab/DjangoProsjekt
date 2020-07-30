from django.db import models

# Create your models here.

class Sum(models.Model):
    '''Modellen for utlegg/inntekter'''
    kategori = models.CharField(default=None, max_length=50)
    sum = models.IntegerField(default=None)
    beskrivelse = models.CharField(default=None, max_length=50)
    date = models.DateField(db_column='Sum_date', blank=True, null=True,
                                verbose_name='Sum_date')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    month = models.IntegerField(default=None)

class Month(models.Model):
    '''modellen for måneder bygd opp av summer.'''