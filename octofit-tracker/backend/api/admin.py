from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'team_id', 'role', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('role', 'created_at')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'activity_type', 'duration', 'calories', 'date')
    list_filter = ('activity_type', 'date')
    search_fields = ('notes',)


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('rank', 'team_name', 'total_points', 'total_activities', 'updated_at')
    ordering = ('rank',)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'duration', 'activity_type', 'calories_estimate')
    list_filter = ('difficulty', 'activity_type')
    search_fields = ('title', 'description')

