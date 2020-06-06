from django.db import models

# Create your models here.


class Movie(models.Model):
    movie_id = models.IntegerField("电影ID", primary_key=True, null=False)
    movie_imdbId = models.CharField("imdb号", max_length=200, null=False)
    movie_title = models.CharField("电影标题", max_length=200, null=False)
    movie_rating = models.DecimalField("电影评分", max_digits=5, decimal_places=1, null=True)
    movie_img = models.CharField("海报", max_length=500, null=True)
    pop = models.IntegerField("观看人数",  default=0, null=False)

    def __str__(self):
        return self.movie_title


class Users(models.Model):
    """用户表"""
    # gender = (
    #     ('male', 'F'),
    #     ('female', 'M'),
    # )
    user_id = models.AutoField(primary_key=True, null=False)
    username = models.CharField(max_length=128, unique=True, null=False)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    # gender = models.CharField(max_length=32, choices=gender, default='M')
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['create_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


class Genres(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    movie_genres = models.CharField(max_length=200)

    def __str__(self):
        return self.movie_genres


class Recommend(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    user_id = models.IntegerField("用户Id")
    movie_id = models.IntegerField("电影Id", null=True)
    movie_imdbId = models.CharField("imdbId", max_length=100, null=True)
    movie_title = models.CharField("电影标题", max_length=100, null=False)
    movie_img = models.CharField("电影图片", max_length=500)


class Rating(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    user_id = models.IntegerField("用户id")
    movie_id = models.IntegerField("电影id")
    movie_imdbId = models.CharField("imdb号", max_length=200, null=False)
    movie_rating = models.DecimalField("电影评分", max_digits=5, decimal_places=1)



