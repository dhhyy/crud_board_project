from django.db import models
from django.db.models.fields.related import ForeignKey

class Board(models.Model):
    writer    = models.ForeignKey('users.User', on_delete=models.CASCADE)
    title     = models.CharField(max_length=45)
    content   = models.CharField(max_length=500)
    password  = models.CharField(max_length=5000, default=None)
    create_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '[{}] {}'.format(self.id, self.title)
    
    class Meta:
        db_table = 'boards'