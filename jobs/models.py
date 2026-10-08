from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):

    ROLE_CHOICES = (
        ('seeker', 'Job Seeker'),
        ('recruiter', 'Recruiter'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='seeker'
    )

    phone = models.CharField(max_length=20, blank=True)

    location = models.CharField(
        max_length=150,
        blank=True
    )

    bio = models.TextField(blank=True)

    company_name = models.CharField(
        max_length=200,
        blank=True
    )

    def __str__(self):
        return self.user.username


class Job(models.Model):

    JOB_TYPES = (
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Internship', 'Internship'),
        ('Remote', 'Remote'),
    )

    title = models.CharField(max_length=200)

    company = models.CharField(
        max_length=200
    )

    location = models.CharField(
        max_length=150
    )

    category = models.CharField(
        max_length=100
    )

    description = models.TextField()

    requirements = models.TextField()

    salary = models.CharField(
        max_length=100,
        blank=True
    )

    job_type = models.CharField(
        max_length=30,
        choices=JOB_TYPES,
        default='Full Time'
    )

    posted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Application(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    applicant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    resume = models.FileField(
        upload_to='resumes/'
    )

    cover_letter = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-applied_at']

    def __str__(self):
        return self.applicant.username