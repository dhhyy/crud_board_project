from django.db import models
from django.db.models.fields.related import ForeignKey

class Category(models.Model):
    name = models.CharField(max_length=45)
    
    def __str__(self):
        return '[{}] {}'.format(self.id, self.name)
    
    class Meta:
        db_table = 'categories'
        
class Tag(models.Model):
    name        = models.CharField(max_length=50, default=None)
    category    = models.ForeignKey('Category', on_delete=models.CASCADE)
    
    def __str__(self):
        return '[{}] {}'.format(self.id, self.name)
    
    class Meta:
        db_table = 'tags'
        
class Board(models.Model):
    writer    = models.ForeignKey('users.User', on_delete=models.CASCADE)
    title     = models.CharField(max_length=45)
    content   = models.CharField(max_length=500)
    password  = models.CharField(max_length=5000, default=None)
    hits      = models.PositiveIntegerField(default=0)
    tag       = models.ForeignKey('Tag', on_delete=models.CASCADE, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '[{}] {}'.format(self.id, self.title)
    
    class Meta:
        db_table = 'boards'