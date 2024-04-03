from django.db import models

GENRES = (
    ('fic', 'Fiction'),
    ('mys', 'Mystery'),
    ('nfc', 'Non-Fiction'),
    ('fan', 'Fantasy'),
    ('tcr', 'True Crime'),
    ('hor', 'Horror'),
    ('his', 'History'),
    ('mem', 'Memoir'),
    ('grn', 'Graphic Novel'),
    ('bio', 'Biography'),
    ('sci', 'Science'),
    ('dra', 'Drama'),
    ('hum', 'Humor'),
    ('adv', 'Adventure'),
    ('rom', 'Romance')
)

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    number_of_works = models.IntegerField()
    still_active = models.BooleanField('Still Active')

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.CharField(max_length=3,
                             choices=GENRES,
                             default=GENRES[0][0])
    description = models.TextField(max_length=500)
    word_count = models.IntegerField('Word Count')
    publication_date = models.DateField('Publication Date')

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-publication_date']