from django.test import TestCase, Client
from django.urls import reverse
from .models import Task
from .forms import TaskForm, TaskEditForm


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


class TaskViewTests(TestCase):
    def setUp(self):
        """Set up test data and client"""
        self.client = Client()
        self.task = Task.objects.create(
            title="Test Task",
            status="open"
        )
        self.task_list_url = reverse('task_list')
        self.edit_task_url = reverse('edit_task', args=[self.task.id])
        self.update_status_url = reverse('update_status', args=[self.task.id])

    def test_task_list_GET(self):
        """Test GET request to task list view"""
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/task_list.html')
        self.assertIn('tasks', response.context)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], TaskForm)

    def test_task_list_POST_valid(self):
        """Test creating a new task via POST"""
        response = self.client.post(self.task_list_url, {
            'title': 'New Test Task',
            'status': 'open'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Task.objects.filter(title='New Test Task').exists())

    def test_task_list_POST_invalid(self):
        """Test creating a task with invalid data"""
        response = self.client.post(self.task_list_url, {
            'title': '',  # Title is required
            'status': 'open'
        })
        self.assertEqual(response.status_code, 200)  # Returns to form
        self.assertFalse(Task.objects.filter(title='').exists())
        form = response.context['form']
        self.assertTrue(form.errors['title'])

    def test_edit_task_GET(self):
        """Test GET request to edit task view"""
        response = self.client.get(self.edit_task_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/edit_task.html')
        self.assertIsInstance(response.context['form'], TaskEditForm)
        self.assertEqual(response.context['task'], self.task)

    def test_edit_task_POST_valid(self):
        """Test editing a task with valid data"""
        response = self.client.post(self.edit_task_url, {
            'title': 'Updated Task Title',
            'status': 'in_progress'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task Title')
        self.assertEqual(self.task.status, 'in_progress')

    def test_edit_task_POST_invalid(self):
        """Test editing a task with invalid data"""
        response = self.client.post(self.edit_task_url, {
            'title': '',  # Title is required
            'status': 'in_progress'
        })
        self.assertEqual(response.status_code, 200)  # Returns to form
        self.task.refresh_from_db()
        self.assertNotEqual(self.task.title, '')  # Title should not be empty

    def test_edit_task_404(self):
        """Test editing a non-existent task"""
        url = reverse('edit_task', args=[99999])  # Non-existent ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_update_status_valid(self):
        """Test updating task status via AJAX"""
        response = self.client.post(self.update_status_url, {
            'status': 'completed'
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'status': 'success',
            'task_status': 'completed',
            'task_status_display': 'Completed',
            'task_id': self.task.id
        })
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, 'completed')

    def test_update_status_invalid_status(self):
        """Test updating task with invalid status"""
        response = self.client.post(self.update_status_url, {
            'status': 'invalid_status'
        })
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertEqual(response_data['status'], 'error')
        self.assertEqual(response_data['message'], 'Invalid status')

    def test_update_status_missing_task(self):
        """Test updating status of non-existent task"""
        url = reverse('update_status', args=[99999])  # Non-existent ID
        response = self.client.post(url, {'status': 'completed'})
        self.assertEqual(response.status_code, 404)
