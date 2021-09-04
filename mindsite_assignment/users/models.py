from django.db import models

class Users(models.Model):

    name = models.CharField(max_length=128, blank=False, null=False, verbose_name='User name',)
    surname = models.CharField(max_length=128, blank=False, null=False, verbose_name='User surname',)
    title = models.CharField(max_length=128, blank=False, null=False, verbose_name='User title',)

    def __str__(self):
        return self.name