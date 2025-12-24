from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify



class Category(models.Model):
    title = models.CharField(max_length=100)


    def __str__(self):
        return self.title

class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, related_name='articles')
    title = models.CharField(max_length=100)
    body = models.TextField()
    image = models.ImageField(upload_to='images/article')
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # float_field = models.FloatField(default=1)
    file_field = models.FileField(upload_to='article',null=True, blank=True)
    slug = models.SlugField(blank=True, unique=True)


    class Meta:
        ordering = ('-updated','-date')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.title)
        super(Article, self).save()


    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})
    
    def body_max(self):
        self.body = self.body[:100]
        return self.body


    def __str__(self):
        return self.title



class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    body = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:50]


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

