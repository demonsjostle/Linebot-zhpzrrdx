from django.db import models

class AutoChat(models.Model):
    question = models.TextField()
    answer = models.TextField()
    class Meta:
        verbose_name_plural = "สคริปต์แชท"
    def __str__(self):
        return self.question
