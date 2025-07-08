from django.db import models
from django.contrib.auth.models import Group, User
from settings_app.models import FacultyProfile , Batch

class Master(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    isactive = models.BooleanField(default=True,verbose_name="Active")
    created_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    class Meta:
        abstract = True
        ordering = ['-isactive']


class Transaction(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    #isactive = models.BooleanField(default=True,verbose_name="Active")
    created_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:       
        abstract = True


METRIC_DATATYPE_CHOICES = [
    ('Number', 'Number'),
    ('Text', 'Text'),
]

class Metric(Master):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    metric_name = models.CharField(max_length=100, verbose_name="Name")
    metric_datatype = models.CharField(max_length=50, choices=METRIC_DATATYPE_CHOICES, verbose_name="Type")

    def __str__(self):
        return f"{self.metric_name} ({self.metric_datatype})"
    
class MilestoneActivity(Master):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    activity = models.CharField(max_length=200)
    day = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.activity} (Day {self.day})"

MONTH_CHOICES = [
    ('January', 'January'),
    ('February', 'February'),
    ('March', 'March'),
    ('April', 'April'),
    ('May', 'May'),
    ('June', 'June'),
    ('July', 'July'),
    ('August', 'August'),
    ('September', 'September'),
    ('October', 'October'),
    ('November', 'November'),
    ('December', 'December'),
]

class FacultyMonthlyReview(Transaction):
    user = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_students = models.IntegerField()
    review_month = models.CharField(max_length=20, choices=MONTH_CHOICES)

    def __str__(self):
        return f"Review: {self.user.username} - {self.batch.name} ({self.review_month})"

class FacultyMonthlyMetric(models.Model):
    monthly_review = models.ForeignKey(FacultyMonthlyReview, on_delete=models.CASCADE)
    metric_name = models.CharField(max_length=200)
    metric_value = models.CharField(max_length=100)

    # def __str__(self):
    #     return f"{self.metric.metric_name}: {self.metric_value} (Review ID: {self.monthly_review.id})"
    
STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Completed', 'Completed'),
]

# class FacultyMonthlyActivity(models.Model):
#     monthly_review = models.ForeignKey(FacultyMonthlyReview, on_delete=models.CASCADE)
#     activity = models.CharField(max_length=200)
#     day = models.CharField(max_length=50)
#     planned_date = models.DateField()
#     completed_date = models.DateField(null=True, blank=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES)
#     participation = models.CharField(max_length=200)
#     remarks = models.CharField(max_length=400)



    # def __str__(self):
    #     return f"{self.activity} ({self.status}) - Review ID: {self.monthly_review.id}"

class FacultyMonthlyActivity(models.Model):
    monthly_review = models.ForeignKey(FacultyMonthlyReview, on_delete=models.CASCADE)

    activity = models.CharField(max_length=200, blank=True, null=True)
    day = models.CharField(max_length=50, blank=True, null=True)

    planned_date = models.DateField(blank=True, null=True)
    completed_date = models.DateField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)
    participation = models.CharField(max_length=200, blank=True, null=True)
    remarks = models.CharField(max_length=400, blank=True, null=True)

    def __str__(self):
        return f"{self.activity or 'No Activity'}"
