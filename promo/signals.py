#TODO: implement django signals for generating thumbnails on image submission.
from io import BytesIO
import logging
from PIL import Image
from django.core.files.base import ContentFile
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import PromoImage

THUMBNAIL_SIZE = (300,300)

logger = logging.getLogger(__name__)
@receiver(pre_save,sender=PromoImage)
def generate_thumbnail(sender,instance,**kwargs):
     logger.info("Generating Thumbnail for product %d",instance.id)
     image = Image.open(instance.image)
     image = image.convert("RGB")
     image.thumbnail(THUMBNAIL_SIZE,Image.ANTIALIAS)
     temp_thumb = BytesIO()
     image.save(temp_thumb,"JPEG")
     temp_thumb.seek(0)
     instance.thumbnail.save(
          instance.image.name,
          ContentFile(temp_thumb.read()),
          save=False
     )
     temp_thumb.close()
     print("Thumbnail generation complete")