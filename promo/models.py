from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Promo(models.Model):
     admin = models.ForeignKey(User,related_name="promos",on_delete=models.CASCADE)
     name = models.CharField(max_length=500,null=False,unique=True)
     details = models.TextField(null=False)
     date = models.DateTimeField(null=False,auto_now_add=True)
     link = models.URLField(max_length=500,null=True)
     

     class Meta:
          ordering = ("-date",)

     def __str__(self) -> str:
          return self.name

class PromoImage(models.Model):
     promo= models.OneToOneField(Promo,related_name='image',on_delete=models.CASCADE)
     image = models.ImageField(upload_to="images",null=True)
     thumbnail = models.ImageField(upload_to="thumbnails",null=True)

     def __str__(self) -> str:
          try:
               return f'{self.thumbnail.url}'
          except Exception as err:
               return f'{self.image.url}'
  

     
