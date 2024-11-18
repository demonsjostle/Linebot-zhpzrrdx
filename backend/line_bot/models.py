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

class ChatRecord(models.Model):
    question = models.TextField()
    answer = models.TextField()
    user = models.CharField(max_length=100, blank=True, null=True)  
    timestamp = models.DateTimeField(auto_now_add=True)  # When the chat record was created 
    source = models.CharField(max_length=100, blank=True, null=True)  # Where the answer was sourced (e.g., AI, human, etc.)

    class Meta:
        verbose_name_plural = "บันทึกแชท"

    def __str__(self):
        return f"ChatRecord({self.user}, {self.timestamp})"



class GPTConfig(models.Model):
    system = models.TextField()
    fine_tuned_model = models.CharField(
        max_length=255, default=None, null=True, blank=True)
    in_use = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "ตั้งค่า GPT"
    def __str__(self):
        return self.system
