from django.db import models
from core.summarize_service import generate_summary

# Create your models here.
class InputText(models.Model):
    title = models.CharField(max_length=500)
    content = models.CharField(max_length=25000)
    summary = models.CharField(max_length=25000, default="")
    rouge = models.CharField(max_length=500, default="")
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "InputText"
    
    def paragraphs(self):
        paragraphs = self.content.split('\n')
        return paragraphs

class WebScrape(models.Model):
    url = models.CharField(max_length=1000)
    # title_news = models.CharField(max_length=5000)
    story = models.CharField(max_length=25000)

    def __str__(self):
        return self.title_news


    
        

