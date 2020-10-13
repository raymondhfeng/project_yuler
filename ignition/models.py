from django.db import models

class IgnitionRow(models.Model):
        num_players_5 = models.IntegerField(default=-1)
        num_players_25 = models.IntegerField(default=-1)
        num_players_50 = models.IntegerField(default=-1)
        num_players_200 = models.IntegerField(default=-1)
        num_players_500 = models.IntegerField(default=-1)
        avg_pot_5 = models.DecimalField(default=-1, max_digits=6, decimal_places=2)
        avg_pot_25 = models.DecimalField(default=-1, max_digits=6, decimal_places=2)
        avg_pot_50 = models.DecimalField(default=-1, max_digits=6, decimal_places=2)
        avg_pot_200 = models.DecimalField(default=-1, max_digits=6, decimal_places=2)
        avg_pot_500 = models.DecimalField(default=-1, max_digits=6, decimal_places=2)
        pct_flop_5 = models.IntegerField(default=-1)
        pct_flop_25 = models.IntegerField(default=-1)
        pct_flop_50 = models.IntegerField(default=-1)
        pct_flop_200 = models.IntegerField(default=-1)
        pct_flop_500 = models.IntegerField(default=-1)
        pub_date = models.DateTimeField('published date')

class IgnitionRowPredictionOLS(IgnitionRow):
    pass

class IgnitionRowPredictionCVX(IgnitionRow):
    pass

COLOR_CHOICES = (
    ('green','GREEN'),
    ('blue', 'BLUE'),
    ('red','RED'),
    ('orange','ORANGE'),
    ('black','BLACK'),
)

class MyModel(models.Model):
  color = models.CharField(max_length=6, choices=COLOR_CHOICES, default='green')

# from django.db import models
from django.contrib.auth.models import User

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
