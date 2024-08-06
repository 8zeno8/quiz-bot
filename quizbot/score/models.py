from django.db import models
from django.utils.translation import gettext as _



class Score(models.Model):
    name =  models.CharField(_("name"), max_length=2550)
    points  = models.IntegerField(_("points"))
    
    
    def __str__(self) -> str:
        return self.name