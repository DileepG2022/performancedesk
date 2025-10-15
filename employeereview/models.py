from django.db import models
from django.contrib.auth.models import Group, User
from settings_app.models import FacultyProfile , Batch , Master, Transaction, Course, SalesProfile, StudentProfile, PlacementProfile
from django.core.validators import MinValueValidator, MaxValueValidator




METRIC_DATATYPE_CHOICES = [
    ('Number', 'Number'),
    ('Text', 'Text'),
]

class Metric(Master):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    metric_name = models.CharField(max_length=100, verbose_name="Name")
    metric_datatype = models.CharField(max_length=50, choices=METRIC_DATATYPE_CHOICES, verbose_name="Type")
    order = models.IntegerField()

    def __str__(self):
        return f"{self.metric_name} ({self.metric_datatype})"
    
class CourseMilestoneActivity(Master):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    activity = models.CharField(max_length=200)
    day = models.IntegerField()
    # order = models.IntegerField()

    def __str__(self):
        return f"{self.activity} (Day {self.day})"

class BatchActivity(Master):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    # course_milestone_activity = models.ForeignKey(CourseMilestoneActivity, on_delete=models.CASCADE)
    activity = models.CharField(max_length=200)
    day = models.IntegerField()
    planned_date = models.DateField()

    def __str__(self):
        # status = " (Completed)" if self.completed else ""
        return f"{self.activity} ({self.batch.name}"

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

class TrainerMonthlyReview(Transaction):
    user = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_students = models.IntegerField()
    # review_month = models.CharField(max_length=20, choices=MONTH_CHOICES)
    review_date = models.DateField(help_text="Month & Year of review")
    remarks = models.CharField(max_length=600, blank=True, null=True)
    def review_month(self):
        return self.review_date.month if self.review_date else None
    def review_year(self):
        return self.review_date.year if self.review_date else None
    def __str__(self):
        return f"Review: {self.user.username} - {self.batch.name} ({self.review_month})"

class TrainerMonthlyMetric(models.Model):
    monthly_review = models.ForeignKey(TrainerMonthlyReview, on_delete=models.CASCADE)
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
    metric_value = models.CharField(max_length=100)

class TrainerMonthlyActivity(models.Model):
    monthly_review = models.ForeignKey(TrainerMonthlyReview, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    completed_date = models.DateField(blank=True, null=True) 
    activity = models.ForeignKey(BatchActivity, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return f"{self.student}"

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

    activity = models.CharField(max_length=200)
    day = models.CharField(max_length=50)

    planned_date = models.DateField()
    completed_date = models.DateField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)
    participation = models.CharField(max_length=200, blank=True, null=True)
    remarks = models.CharField(max_length=400, blank=True, null=True)

    def __str__(self):
        return f"{self.activity or 'No Activity'}"

class SalesMonthlyReview(Transaction):
    user = models.ForeignKey(SalesProfile, on_delete=models.CASCADE)
    review_date = models.DateField(help_text="Month & Year of review")
    remarks = models.CharField(max_length=600, blank=True, null=True)
    def review_month(self):
        return self.review_date.month if self.review_date else None
    def review_year(self):
        return self.review_date.year if self.review_date else None
    def __str__(self):
        return f"Review: {self.user.username} - {self.review_month} {self.review_year}"

class SalesMonthlyMetric(models.Model):
    monthly_review = models.ForeignKey(SalesMonthlyReview, on_delete=models.CASCADE)
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
    metric_value = models.CharField(max_length=100)

class PlacementMonthlyReview(Transaction):
    user = models.ForeignKey(PlacementProfile, on_delete=models.CASCADE)
    # batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    # start_date = models.DateField()
    # end_date = models.DateField()
    # total_students = models.IntegerField()
    # # review_month = models.CharField(max_length=20, choices=MONTH_CHOICES)
    review_date = models.DateField(help_text="Month & Year of review")
    remarks = models.CharField(max_length=600, blank=True, null=True)
    def review_month(self):
        return self.review_date.month if self.review_date else None
    def review_year(self):
        return self.review_date.year if self.review_date else None
    def __str__(self):
        return f"Review: {self.user.username} - {self.batch.name} ({self.review_month})"

class PlacementMonthlyMetric(models.Model):
    monthly_review = models.ForeignKey(PlacementMonthlyReview, on_delete=models.CASCADE)
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
    metric_value = models.CharField(max_length=100)

# class PlacementPool(Transaction):
#     student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)

#     placed_date = models.DateField(blank=True, null=True) 
#     activity = models.ForeignKey(BatchActivity, on_delete=models.CASCADE)
    
    
#     def __str__(self):
#         return f"{self.student}"

class SalesTarget(Transaction):
    sales_person = models.ForeignKey(
        SalesProfile,
        on_delete=models.CASCADE,
        related_name="sales_targets"
    )
    target_date = models.DateField(help_text="Select month & year for target")
    target_value = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Enter monthly target (e.g. 100 leads, deals, etc.)"
    )

    class Meta:
        unique_together = ('sales_person', 'target_date')
        ordering = ['-target_date']

    def __str__(self):
        return f"{self.sales_person} → {self.target_date.strftime('%B %Y')}: {self.target_value}"