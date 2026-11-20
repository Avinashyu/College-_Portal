from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Student_table


class CollegePortalTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='StrongPass123!',
        )

    def test_home_and_login_pages_load(self):
        self.assertEqual(self.client.get(reverse('home')).status_code, 200)
        self.assertEqual(self.client.get(reverse('login')).status_code, 200)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('dashboard')}",
        )

    def test_student_form_creates_student(self):
        response = self.client.post(reverse('student_form'), {
            'reg_no': 101,
            'name': 'Student One',
            'email': 'student@example.com',
            'marks': '88.50',
            'date': '2005-06-15',
        })
        self.assertRedirects(response, reverse('student_form'))
        self.assertTrue(
            Student_table.objects.filter(reg_no=101, name='Student One').exists()
        )

    def test_duplicate_registration_number_is_rejected(self):
        Student_table.objects.create(
            reg_no=101,
            name='Existing',
            email='existing@example.com',
            marks='75.00',
            date='2005-01-01',
        )
        response = self.client.post(reverse('student_form'), {
            'reg_no': 101,
            'name': 'Duplicate',
            'email': 'duplicate@example.com',
            'marks': '80.00',
            'date': '2005-02-02',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'already registered')

    def test_api_lists_students(self):
        Student_table.objects.create(
            reg_no=102,
            name='API Student',
            email='api@example.com',
            marks='91.25',
            date='2004-03-10',
        )
        response = self.client.get(reverse('student-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['reg_no'], 102)
