from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Student


class TeacherPortalTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = 'rajat2'
        self.password = '1234'
        self.user = User.objects.create_user(username=self.username, password=self.password)

        self.student = Student.objects.create(name='karan', subject='Math', marks=50)

    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_fail(self):
        response = self.client.post(reverse('login'), {
            'username': 'rajat',
            'password': '1111'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid credentials')

    def test_dashboard_shows_students(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'karan')
        self.assertContains(response, 'Math')

    def test_add_student(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('add_student'), {
            'name': 'Hi',
            'subject': 'Science',
            'marks': '40'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Student.objects.filter(name='Hi', subject='Science').exists())

    def test_add_same_student_updates_marks(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('add_student'), {
            'name': 'karan',
            'subject': 'Math',
            'marks': '10'
        })
        self.assertEqual(response.status_code, 302)
        updated_std = Student.objects.get(name='karan', subject='Math')
        self.assertEqual(updated_std.marks, 60)

    def test_delete_student(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('delete_student', args=[self.student.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Student.objects.filter(id=self.student.id).exists())

    def test_register_user_success(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password': 'test1234',
            'confirm_password': 'test1234'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_password_not_match(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password': 'test1234',
            'confirm_password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Passwords do not match')
