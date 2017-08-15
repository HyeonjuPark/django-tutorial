from django.db import models
from django.utils import timezone
from dynamic_scraper.models import Scraper, SchedulerRuntime
from scrapy_djangoitem import DjangoItem
from django.dispatch import receiver
from django.db.models.signals import pre_delete

@receiver(pre_delete)
def pre_delete_handler(sender, instance, using, **kwargs):
    if isinstance(instance, Post):
        if instance.checker_runtime:
            instance.checker_runtime.delete()

pre_delete.connect(pre_delete_handler)

class PostSite(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    scraper = models.ForeignKey(Scraper, blank=True, null=True, on_delete=models.SET_NULL)
    scraper_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey('auth.User',
                               blank=True,
                               null=True,)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    image = models.CharField(max_length=200)
    post_site = models.ForeignKey(PostSite)
    url = models.URLField()
    checker_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)
    foo = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    def setfoo(self, x):
        self.foo = json.dumps(x)

    def getfoo(self):
        return json.loads(self.foo)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class PostItem(DjangoItem):
    django_model = Post