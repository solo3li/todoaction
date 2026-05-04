from django.test import TestCase
from django.contrib.auth.models import User
from .models import Todo

class TodoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_todo_creation(self):
        todo = Todo.objects.create(user=self.user, title="Test Todo")
        self.assertEqual(todo.title, "Test Todo")
        self.assertFalse(todo.completed)
        self.assertEqual(todo.user.username, 'testuser')

    def test_todo_str(self):
        todo = Todo.objects.create(user=self.user, title="Test Todo")
        self.assertEqual(str(todo), "Test Todo")

class TodoViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_todo_list_view_authenticated(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My Tasks")

    def test_todo_list_view_unauthenticated(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)  # Redirects to login
