from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Course(models.Model):
    #id: auto
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    # if a user is deleted and then his posts should be deleted as well
    posted_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)

class Like(models.Model):
    user = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', related_name='likes', on_delete=models.CASCADE)