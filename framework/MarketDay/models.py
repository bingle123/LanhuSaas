from django.db import models

class Holiday(models.Model):
    day=models.CharField(max_length=30,primary_key=True)
    def __unicode__(self):
        return self.day
    class Meta:
        db_table='holiday'