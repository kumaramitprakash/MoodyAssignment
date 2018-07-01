from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

def validate_non_zero(value):
    if value == 0:
        raise ValidationError(('%(value)s is less than 1'), params={'value': value},)
        
class MedalTable(models.Model):
    rank = models.PositiveSmallIntegerField(validators=[validate_non_zero])
    country = models.CharField(primary_key=True, max_length=20)
    gold = models.PositiveSmallIntegerField()
    silver = models.PositiveSmallIntegerField()
    bronze = models.PositiveSmallIntegerField()
    total = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return self.country
    
    
    
