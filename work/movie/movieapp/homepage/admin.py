from django.contrib import admin
from .models import Movie, Users, Genres

# Register your models here.
# admin.site.register(Movie)
admin.site.register(Users)


class GenresInline(admin.TabularInline):
    model = Genres
    extra = 6


class MovieAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['movie_id', 'movie_imdbId', 'movie_title', 'movie_rating', 'movie_img', 'pop']}),
    ]
    inlines = [GenresInline]
    list_display = ('movie_title', 'movie_id', 'movie_rating')
    search_fields = ['movie_id', 'movie_title','movie_imdbId']


admin.site.register(Movie, MovieAdmin)
