from django.db import models

class AutoChat(models.Model):
    question = models.TextField()
    answer = models.TextField()
    class Meta:
        verbose_name_plural = "สคริปต์แชท"
    def __str__(self):
        return self.question

class Notification(models.Model):
    name = models.CharField(max_length=250, default=None, blank=True, null=True)
    user_name = models.CharField(max_length=250, default=None, blank=True, null=True)
    line_uid = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "การแจ้งเตือน"

    def __str__(self):
        if self.name:
            return self.name 
        else:
            return self.line_uid

