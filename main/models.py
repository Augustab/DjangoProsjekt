from django.db import models

# Create your models here.


   # def __str__(self):
   #     return "Bruker: " + str(self.user.username) + \
   #         " -- verdi: " + str(self.sum) + " -- måned: "


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

   # def __str__(self):
    #    return "Name: " + str(self.name) + \
    #        " -- user:" + str(self.user.username)

#Account.objects.get(name="Default").accountid
class Sum(models.Model):
    '''Modellen for utlegg/inntekter'''
    account = models.ForeignKey('Account', on_delete=models.CASCADE, default=None)
    sum = models.IntegerField(default=None)
    beskrivelse = models.CharField(default=None, max_length=50)
    date = models.DateField(db_column='Sum_date', blank=True, null=True,
                                verbose_name='Sum_date')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    month = models.IntegerField(default=None)
    sumid = models.AutoField(db_column='sumid', primary_key=True)
