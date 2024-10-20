from django.db import models
class Tag(models.Model):
    tag_name = models.CharField(max_length=100)  # Make sure to set max_length
    class Meta:
        verbose_name_plural = "แท็ก"
    def __str__(self):
        return self.tag_name
class AutoChat(models.Model):
    question = models.TextField()
    answer = models.TextField()
    image = models.ImageField(upload_to='auto-chats/', blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='auto_chats', blank=True)
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

