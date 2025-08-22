
from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
class Querry(models.Model):
    query_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=122)
    email = models.EmailField(max_length=122)
    desc = models.TextField()
    date = models.DateField(default=date.today)
    Cat = models.CharField(max_length=20, default='Other')
    view_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.query_id}"

class Signup(models.Model):
    name = models.CharField(max_length=30,default='xyz')
    password = models.CharField(max_length=15,default='123')
    email = models.EmailField(max_length=40, default='sample@gmail.com')
    Year = models.CharField(max_length=10, default='2')
    Branch = models.CharField(max_length=20, default='IT')  
    date = models.DateField()
    
    def __str__(self):
        return self.name
    
class Answers(models.Model):
    answer_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.ForeignKey(Querry,related_name='answers', on_delete=models.CASCADE)
    response = models.TextField()
    rating = models.IntegerField(default=0)
    date = models.DateField(default=date.today)


    def __str__(self):
        return (
            f"Answer ID:- {self.answer_id},\n"
            f"Query ID:- {self.query},\n"
            f"Date:- {self.date},"
        )
    
class Rating(models.Model):
    answer = models.ForeignKey(Answers, on_delete=models.CASCADE, related_name='ratings')
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who is rating
    rating_value = models.IntegerField(default=0)
    date = models.DateField(default=date.today)

    class Meta:
        unique_together = ('answer', 'rated_by')  # Ensures one user can rate an answer only once.

    def __str__(self):
        return f"Rating: {self.rating_value} by {self.rated_by.username} for Answer ID: {self.answer.answer_id}"



    
       
