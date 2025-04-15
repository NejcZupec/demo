from django.test import TestCase
from .models import Task

class TaskModelTests(TestCase):
    def test_task_creation(self):
        """Test that we can create a task"""
        task = Task.objects.create(title="Test Task", status="open")
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.status, "open")
    
    def test_task_str(self):
        """Test the string representation of a task"""
        task = Task.objects.create(title="Another Test Task", status="in_progress")
        self.assertEqual(str(task), "Another Test Task")
    
    def test_task_status_choices(self):
        """Test that task status must be one of the valid choices"""
        task = Task.objects.create(title="Test Task", status="open")
        self.assertIn(task.status, ["open", "in_progress", "in_review", "completed"])
