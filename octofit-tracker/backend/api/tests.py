from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Team, Activity, Leaderboard, Workout


class UserModelTest(TestCase):
    """Test cases for User model."""
    
    def setUp(self):
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            team_id=1,
            role='member'
        )
    
    def test_user_creation(self):
        """Test user is created correctly."""
        self.assertEqual(self.user.name, 'Test User')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.team_id, 1)
        self.assertEqual(self.user.role, 'member')
    
    def test_user_str(self):
        """Test user string representation."""
        self.assertEqual(str(self.user), 'Test User')


class TeamModelTest(TestCase):
    """Test cases for Team model."""
    
    def setUp(self):
        self.team = Team.objects.create(
            name='Team Marvel',
            description='Earth\'s Mightiest Heroes'
        )
    
    def test_team_creation(self):
        """Test team is created correctly."""
        self.assertEqual(self.team.name, 'Team Marvel')
        self.assertEqual(self.team.description, 'Earth\'s Mightiest Heroes')
    
    def test_team_str(self):
        """Test team string representation."""
        self.assertEqual(str(self.team), 'Team Marvel')


class ActivityModelTest(TestCase):
    """Test cases for Activity model."""
    
    def setUp(self):
        self.activity = Activity.objects.create(
            user_id=1,
            activity_type='running',
            duration=30,
            calories=300,
            distance=5.0,
            date=timezone.now()
        )
    
    def test_activity_creation(self):
        """Test activity is created correctly."""
        self.assertEqual(self.activity.activity_type, 'running')
        self.assertEqual(self.activity.duration, 30)
        self.assertEqual(self.activity.calories, 300)
        self.assertEqual(self.activity.distance, 5.0)


class LeaderboardModelTest(TestCase):
    """Test cases for Leaderboard model."""
    
    def setUp(self):
        self.entry = Leaderboard.objects.create(
            team_id=1,
            team_name='Team Marvel',
            total_points=1000,
            total_activities=50,
            rank=1
        )
    
    def test_leaderboard_creation(self):
        """Test leaderboard entry is created correctly."""
        self.assertEqual(self.entry.team_name, 'Team Marvel')
        self.assertEqual(self.entry.total_points, 1000)
        self.assertEqual(self.entry.rank, 1)


class WorkoutModelTest(TestCase):
    """Test cases for Workout model."""
    
    def setUp(self):
        self.workout = Workout.objects.create(
            title='Morning Run',
            description='Easy morning jog',
            difficulty='beginner',
            duration=30,
            activity_type='running',
            calories_estimate=250,
            instructions='Warm up, then run at steady pace'
        )
    
    def test_workout_creation(self):
        """Test workout is created correctly."""
        self.assertEqual(self.workout.title, 'Morning Run')
        self.assertEqual(self.workout.difficulty, 'beginner')
        self.assertEqual(self.workout.duration, 30)


class UserAPITest(APITestCase):
    """Test cases for User API endpoints."""
    
    def test_create_user(self):
        """Test creating a user via API."""
        data = {
            'name': 'API User',
            'email': 'api@example.com',
            'team_id': 1,
            'role': 'member'
        }
        response = self.client.post('/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, 'API User')
    
    def test_list_users(self):
        """Test listing users via API."""
        User.objects.create(name='User 1', email='user1@example.com')
        User.objects.create(name='User 2', email='user2@example.com')
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class TeamAPITest(APITestCase):
    """Test cases for Team API endpoints."""
    
    def test_create_team(self):
        """Test creating a team via API."""
        data = {'name': 'API Team', 'description': 'Test team'}
        response = self.client.post('/teams/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 1)
    
    def test_list_teams(self):
        """Test listing teams via API."""
        Team.objects.create(name='Team 1')
        Team.objects.create(name='Team 2')
        response = self.client.get('/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class APIRootTest(APITestCase):
    """Test case for API root endpoint."""
    
    def test_api_root(self):
        """Test that API root is accessible and returns expected endpoints."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the root contains links to our endpoints
        self.assertIn('users', response.data)
        self.assertIn('teams', response.data)
        self.assertIn('activities', response.data)
        self.assertIn('leaderboard', response.data)
        self.assertIn('workouts', response.data)
