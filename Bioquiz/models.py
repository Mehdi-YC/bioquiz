from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
import os

class UserDetails(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    score = models.IntegerField(default=0)



class Image(models.Model):
    image_file = models.ImageField(upload_to='static/media')
    image_name = models.CharField(max_length=50,null=False)
    description = models.TextField()
    microscopy = models.CharField(max_length=50,null=False)
    cell_type = models.CharField(max_length=50,null=False)
    component = models.CharField(max_length=50,null=False)
    doi = models.CharField(max_length=50,null=False)
    organism = models.CharField(max_length=50,null=False)

    def get_remote_image(self):
        if self.image_url and not self.image_file:
            result = urllib.urlretrieve(self.image_url)
            self.image_file.save(
                    os.path.basename(self.image_url),
                    File(open(result[0]))
                    )
            self.save()




class Answer(models.Model):
    question_id = models.IntegerField(null=False)
    answer = models.CharField(max_length=50,null=False)
    definition = models.TextField()

class Question(models.Model):
    question = models.CharField(max_length=200,null=False)
    category = models.CharField(max_length=50,null=False)
    imageField = models.CharField(max_length=50,null=False)
    point = models.IntegerField(default=3)
    n_answer = models.IntegerField(default=0)
    n_image = models.IntegerField(default=0)
    Quiz_name = models.CharField(max_length=200,null=False)
    id_images = models.CharField(max_length=200,null=False)
    Correct_answer = models.IntegerField(null=False) 