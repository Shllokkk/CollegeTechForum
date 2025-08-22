
from django.db import models
from django.db.models import F, Avg
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
class Querry(models.Model):
    """A user-submitted question in the forum.

    Note: Field names and types are preserved to avoid migrations.
    """
    query_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=122)
    email = models.EmailField(max_length=122)
    desc = models.TextField()
    date = models.DateField(default=date.today)
    Cat = models.CharField(max_length=20, default='Other')
    view_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Query #{self.query_id} by {self.name} ({self.Cat})"

    def __repr__(self) -> str:
        return (
            f"Querry(query_id={self.query_id}, user_id={getattr(self.user, 'id', None)}, "
            f"name={self.name!r}, Cat={self.Cat!r}, view_count={self.view_count})"
        )

    def increment_view_count(self, amount: int = 1) -> None:
        """Atomically increment view_count by amount (default 1)."""
        if amount == 0:
            return
        Querry.objects.filter(pk=self.pk).update(view_count=F('view_count') + amount)
        # Keep instance in sync if reused after call
        self.view_count += amount

    @property
    def num_answers(self) -> int:
        """Number of answers for this query."""
        return self.answers.count()

    @property
    def average_answer_rating(self):
        """Average rating across all answers' ratings for this query.

        Uses the related `Rating` objects via `Answers` relation. Returns None if no ratings.
        """
        return (
            Rating.objects.filter(answer__query=self).aggregate(avg=Avg('rating_value'))['avg']
        )

class Signup(models.Model):
    """Lightweight signup info (separate from auth `User`)."""
    name = models.CharField(max_length=30,default='xyz')
    password = models.CharField(max_length=15,default='123')
    email = models.EmailField(max_length=40, default='sample@gmail.com')
    Year = models.CharField(max_length=10, default='2')
    Branch = models.CharField(max_length=20, default='IT')  
    date = models.DateField()
    
    def __str__(self):
        return self.name
    
    def __repr__(self) -> str:
        return (
            f"Signup(name={self.name!r}, email={self.email!r}, Year={self.Year!r}, "
            f"Branch={self.Branch!r}, date={self.date!r})"
        )
    
class Answers(models.Model):
    """An answer posted by a user in response to a `Querry`."""
    answer_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.ForeignKey(Querry,related_name='answers', on_delete=models.CASCADE)
    response = models.TextField()
    rating = models.IntegerField(default=0)
    date = models.DateField(default=date.today)


    def __str__(self):
        return f"Answer #{self.answer_id} for Query #{getattr(self.query, 'query_id', None)} on {self.date}"

    def __repr__(self) -> str:
        return (
            f"Answers(answer_id={self.answer_id}, query_id={getattr(self.query, 'query_id', None)}, "
            f"user_id={getattr(self.user, 'id', None)}, date={self.date!r})"
        )

    @property
    def num_ratings(self) -> int:
        """Number of user ratings for this answer."""
        return self.ratings.count()

    @property
    def average_rating(self):
        """Average of `Rating.rating_value` for this answer; None if no ratings."""
        return self.ratings.aggregate(avg=Avg('rating_value'))['avg']
    
class Rating(models.Model):
    """A user's rating on a specific `Answers` entry."""
    answer = models.ForeignKey(Answers, on_delete=models.CASCADE, related_name='ratings')
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who is rating
    rating_value = models.IntegerField(default=0)
    date = models.DateField(default=date.today)

    class Meta:
        unique_together = ('answer', 'rated_by')  # Ensures one user can rate an answer only once.

    def __str__(self):
        return f"Rating: {self.rating_value} by {self.rated_by.username} for Answer ID: {self.answer.answer_id}"

    def __repr__(self) -> str:
        return (
            f"Rating(answer_id={getattr(self.answer, 'answer_id', None)}, "
            f"rated_by_id={getattr(self.rated_by, 'id', None)}, value={self.rating_value})"
        )