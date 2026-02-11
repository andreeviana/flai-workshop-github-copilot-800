from django.db import models


class User(models.Model):
    """User model for OctoFit tracker."""
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    team_id = models.IntegerField(null=True, blank=True)
    role = models.CharField(max_length=100, default='member')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name


class Team(models.Model):
    """Team model for organizing users."""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name


class Activity(models.Model):
    """Activity model for tracking user workouts."""
    user_id = models.IntegerField()
    activity_type = models.CharField(max_length=100)
    duration = models.IntegerField(help_text='Duration in minutes')
    calories = models.IntegerField(help_text='Calories burned')
    distance = models.FloatField(default=0.0, help_text='Distance in kilometers')
    date = models.DateTimeField()
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'activities'
        verbose_name_plural = 'Activities'

    def __str__(self):
        return f'{self.activity_type} - {self.duration} min'


class Leaderboard(models.Model):
    """Leaderboard model for tracking team rankings."""
    team_id = models.IntegerField(unique=True)
    team_name = models.CharField(max_length=200)
    total_points = models.IntegerField(default=0)
    total_activities = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leaderboard'
        ordering = ['-total_points']

    def __str__(self):
        return f'{self.team_name} - {self.total_points} points'


class Workout(models.Model):
    """Workout model for personalized workout suggestions."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(
        max_length=50,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced')
        ]
    )
    duration = models.IntegerField(help_text='Suggested duration in minutes')
    activity_type = models.CharField(max_length=100)
    calories_estimate = models.IntegerField(help_text='Estimated calories burned')
    instructions = models.TextField()

    class Meta:
        db_table = 'workouts'

    def __str__(self):
        return f'{self.title} ({self.difficulty})'

