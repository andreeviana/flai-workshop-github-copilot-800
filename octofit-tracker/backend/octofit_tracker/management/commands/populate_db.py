from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from api.models import User, Team, Activity, Leaderboard, Workout
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Deleting existing data...'))
        
        # Delete all existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('Existing data deleted.'))
        
        # Create Teams
        self.stdout.write(self.style.WARNING('Creating teams...'))
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Avengers assemble! Earth\'s mightiest heroes working together to achieve peak fitness.'
        )
        team_dc = Team.objects.create(
            name='Team DC',
            description='Justice League united! The world\'s finest heroes combining strength and discipline.'
        )
        self.stdout.write(self.style.SUCCESS(f'Created teams: {team_marvel.name}, {team_dc.name}'))
        
        # Create Users (Superheroes)
        self.stdout.write(self.style.WARNING('Creating users...'))
        marvel_heroes = [
            {'name': 'Tony Stark', 'email': 'iron.man@marvel.com', 'role': 'team_leader'},
            {'name': 'Steve Rogers', 'email': 'captain.america@marvel.com', 'role': 'member'},
            {'name': 'Natasha Romanoff', 'email': 'black.widow@marvel.com', 'role': 'member'},
            {'name': 'Bruce Banner', 'email': 'hulk@marvel.com', 'role': 'member'},
            {'name': 'Thor Odinson', 'email': 'thor@marvel.com', 'role': 'member'},
            {'name': 'Peter Parker', 'email': 'spider.man@marvel.com', 'role': 'member'},
            {'name': 'Wanda Maximoff', 'email': 'scarlet.witch@marvel.com', 'role': 'member'},
            {'name': 'Carol Danvers', 'email': 'captain.marvel@marvel.com', 'role': 'member'},
        ]
        
        dc_heroes = [
            {'name': 'Bruce Wayne', 'email': 'batman@dc.com', 'role': 'team_leader'},
            {'name': 'Clark Kent', 'email': 'superman@dc.com', 'role': 'member'},
            {'name': 'Diana Prince', 'email': 'wonder.woman@dc.com', 'role': 'member'},
            {'name': 'Barry Allen', 'email': 'flash@dc.com', 'role': 'member'},
            {'name': 'Arthur Curry', 'email': 'aquaman@dc.com', 'role': 'member'},
            {'name': 'Hal Jordan', 'email': 'green.lantern@dc.com', 'role': 'member'},
            {'name': 'Victor Stone', 'email': 'cyborg@dc.com', 'role': 'member'},
            {'name': 'Kara Zor-El', 'email': 'supergirl@dc.com', 'role': 'member'},
        ]
        
        marvel_users = []
        for hero in marvel_heroes:
            user = User.objects.create(
                name=hero['name'],
                email=hero['email'],
                team_id=team_marvel.id,
                role=hero['role']
            )
            marvel_users.append(user)
            self.stdout.write(f'  Created Marvel hero: {user.name}')
        
        dc_users = []
        for hero in dc_heroes:
            user = User.objects.create(
                name=hero['name'],
                email=hero['email'],
                team_id=team_dc.id,
                role=hero['role']
            )
            dc_users.append(user)
            self.stdout.write(f'  Created DC hero: {user.name}')
        
        all_users = marvel_users + dc_users
        self.stdout.write(self.style.SUCCESS(f'Created {len(all_users)} superhero users.'))
        
        # Create Activities
        self.stdout.write(self.style.WARNING('Creating activities...'))
        activity_types = ['Running', 'Cycling', 'Swimming', 'Strength Training', 'Yoga', 'Boxing', 'HIIT']
        
        activity_count = 0
        for user in all_users:
            # Create 5-10 activities per user
            num_activities = random.randint(5, 10)
            for i in range(num_activities):
                activity_type = random.choice(activity_types)
                duration = random.randint(20, 120)
                calories = duration * random.randint(5, 12)
                distance = round(random.uniform(1, 15), 2) if activity_type in ['Running', 'Cycling', 'Swimming'] else 0
                
                Activity.objects.create(
                    user_id=user.id,
                    activity_type=activity_type,
                    duration=duration,
                    calories=calories,
                    distance=distance,
                    date=timezone.now() - timedelta(days=random.randint(0, 30)),
                    notes=f'{user.name} completed {activity_type} session'
                )
                activity_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {activity_count} activities.'))
        
        # Create Leaderboard entries
        self.stdout.write(self.style.WARNING('Creating leaderboard entries...'))
        
        # Calculate Marvel team stats
        marvel_activities = Activity.objects.filter(user_id__in=[u.id for u in marvel_users])
        marvel_points = sum(a.calories for a in marvel_activities)
        marvel_activity_count = marvel_activities.count()
        
        # Calculate DC team stats
        dc_activities = Activity.objects.filter(user_id__in=[u.id for u in dc_users])
        dc_points = sum(a.calories for a in dc_activities)
        dc_activity_count = dc_activities.count()
        
        # Determine ranks
        if marvel_points > dc_points:
            marvel_rank, dc_rank = 1, 2
        elif dc_points > marvel_points:
            marvel_rank, dc_rank = 2, 1
        else:
            marvel_rank, dc_rank = 1, 1
        
        Leaderboard.objects.create(
            team_id=team_marvel.id,
            team_name=team_marvel.name,
            total_points=marvel_points,
            total_activities=marvel_activity_count,
            rank=marvel_rank
        )
        
        Leaderboard.objects.create(
            team_id=team_dc.id,
            team_name=team_dc.name,
            total_points=dc_points,
            total_activities=dc_activity_count,
            rank=dc_rank
        )
        
        self.stdout.write(self.style.SUCCESS(
            f'Created leaderboard: {team_marvel.name} ({marvel_points} pts, rank {marvel_rank}), '
            f'{team_dc.name} ({dc_points} pts, rank {dc_rank})'
        ))
        
        # Create Workouts
        self.stdout.write(self.style.WARNING('Creating workout suggestions...'))
        workouts = [
            {
                'title': 'Super Soldier Strength Training',
                'description': 'Build strength like Captain America with this comprehensive workout.',
                'difficulty': 'advanced',
                'duration': 60,
                'activity_type': 'Strength Training',
                'calories_estimate': 500,
                'instructions': '1. Warm up (10 min)\n2. Bench press 4x10\n3. Squats 4x12\n4. Deadlifts 3x8\n5. Pull-ups 3x15\n6. Cool down (5 min)'
            },
            {
                'title': 'Speed Force Cardio',
                'description': 'Train your speed and endurance like The Flash.',
                'difficulty': 'intermediate',
                'duration': 45,
                'activity_type': 'Running',
                'calories_estimate': 600,
                'instructions': '1. Dynamic stretching (5 min)\n2. Sprint intervals 8x100m\n3. Recovery jog 2 min between sprints\n4. Cool down jog (10 min)'
            },
            {
                'title': 'Warrior Princess Combat Training',
                'description': 'Channel Wonder Woman with martial arts and combat fitness.',
                'difficulty': 'advanced',
                'duration': 75,
                'activity_type': 'Boxing',
                'calories_estimate': 700,
                'instructions': '1. Shadow boxing (10 min)\n2. Heavy bag work (20 min)\n3. Speed bag (10 min)\n4. Core work (15 min)\n5. Stretching (20 min)'
            },
            {
                'title': 'Zen Master Flexibility',
                'description': 'Find balance and flexibility with this yoga routine.',
                'difficulty': 'beginner',
                'duration': 30,
                'activity_type': 'Yoga',
                'calories_estimate': 150,
                'instructions': '1. Breathing exercises (5 min)\n2. Sun salutations (10 min)\n3. Warrior poses (10 min)\n4. Savasana (5 min)'
            },
            {
                'title': 'Asgardian Thunder Workout',
                'description': 'Build god-like strength with Thor\'s favorite exercises.',
                'difficulty': 'advanced',
                'duration': 90,
                'activity_type': 'Strength Training',
                'calories_estimate': 800,
                'instructions': '1. Battle rope slams (5 min)\n2. Hammer curls 4x12\n3. Overhead press 4x10\n4. Farmers walk 4x50m\n5. Norse mythology reading (cool down)'
            },
            {
                'title': 'Web-Slinger Agility Training',
                'description': 'Improve agility and reflexes like Spider-Man.',
                'difficulty': 'intermediate',
                'duration': 40,
                'activity_type': 'HIIT',
                'calories_estimate': 450,
                'instructions': '1. Jump rope (5 min)\n2. Burpees 3x15\n3. Box jumps 3x20\n4. Mountain climbers 3x30\n5. Plank holds 3x60s'
            },
            {
                'title': 'Atlantean Swimming Power',
                'description': 'Master the water with Aquaman\'s swimming workout.',
                'difficulty': 'intermediate',
                'duration': 50,
                'activity_type': 'Swimming',
                'calories_estimate': 550,
                'instructions': '1. Warm up (200m easy)\n2. Main set: 10x100m freestyle\n3. Kick drills (10 min)\n4. Pull drills (10 min)\n5. Cool down (200m easy)'
            },
            {
                'title': 'Dark Knight Urban Cycling',
                'description': 'Build endurance on two wheels like Batman patrols Gotham.',
                'difficulty': 'beginner',
                'duration': 35,
                'activity_type': 'Cycling',
                'calories_estimate': 350,
                'instructions': '1. Easy spin warm up (5 min)\n2. Moderate pace (20 min)\n3. Hill climbs (5 min)\n4. Cool down (5 min)'
            },
        ]
        
        for workout_data in workouts:
            workout = Workout.objects.create(**workout_data)
            self.stdout.write(f'  Created workout: {workout.title}')
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(workouts)} workout suggestions.'))
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('Database population complete!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(f'Teams: {Team.objects.count()}')
        self.stdout.write(f'Users: {User.objects.count()}')
        self.stdout.write(f'Activities: {Activity.objects.count()}')
        self.stdout.write(f'Leaderboard entries: {Leaderboard.objects.count()}')
        self.stdout.write(f'Workouts: {Workout.objects.count()}')
        self.stdout.write(self.style.SUCCESS('='*60))
