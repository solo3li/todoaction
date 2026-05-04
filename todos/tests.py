from django.test import TestCase
from .models import Todo

class TodoModelTest(TestCase):
    def test_todo_creation(self):
        todo = Todo.objects.create(title="Test Todo")
        self.assertEqual(todo.title, "Test Todo")
        self.assertFalse(todo.completed)

    def test_todo_str(self):
        todo = Todo.objects.create(title="Test Todo")
        self.assertEqual(str(todo), "Test Todo")

class TodoViewTest(TestCase):
    def test_todo_list_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Todo List")
