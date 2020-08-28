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
    sumid = models.AutoField(db_column='sumid', primary_key=True)

class Month(models.Model):
    ##sums = models.QuerySet
    ##monthid = models.IntegerField
    '''modellen for måneder bygd opp av summer.'''


class Account(models.Model):
    '''Modellen for kontoer'''
    name = models.CharField(default=None, max_length=50)
    belop = models.IntegerField(default=0)
    interest = models.CharField(default=None, max_length=50)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    accountid = models.AutoField(db_column='accountid', primary_key=True)