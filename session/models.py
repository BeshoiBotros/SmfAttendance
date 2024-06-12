from django.db import models
from accounts import models as accounts_models
from django.utils.timezone import datetime
class Session(models.Model):
    
    admin    = models.ForeignKey(accounts_models.Admin, on_delete=models.CASCADE)
    name     = models.CharField(max_length=255)
    students = models.ManyToManyField(accounts_models.Student, blank=True)
    start_at = models.DateTimeField(default=datetime.now)
    end_at   = models.DateTimeField()

    def __str__(self):
        return self.name
    
