
from django.db import models
from companies.models import CompanyProfile


class Job(models.Model):

    company = models.ForeignKey(
        CompanyProfile,
        on_delete=models.CASCADE,
        related_name="jobs"
    )

    title = models.CharField(max_length=150)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=100)

    salary = models.CharField(max_length=50)
    job_type = models.CharField(max_length=50)

    vacancies = models.PositiveIntegerField(default=1)

    posted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


from candidates.models import CandidateProfile


class Application(models.Model):

    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Under Review', 'Under Review'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
        ('Selected', 'Selected'),
    ]

    candidate = models.ForeignKey(
        CandidateProfile,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    applied_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Applied'
    )

    class Meta:
        unique_together = ('candidate', 'job')

    def __str__(self):
        return f"{self.candidate.user.username} - {self.job.title}"
