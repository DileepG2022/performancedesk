from django.db import models
from django.contrib.auth.models import User
import os
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
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

class Branch(Master):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Course(Master):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class FacultyProfile(Master):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="faculty_user")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)  # Faculty can teach multiple courses
    mobile_no = PhoneNumberField(null=True, blank=True, region='IN')  # 'IN' for India
    whatsapp_no = PhoneNumberField(null=True, blank=True, region='IN')
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="faculty_creator")

    def __str__(self):
        return f"Faculty: {self.user.username} ({self.branch.name})"


class Batch(Master):
    name = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE)  # 🔥 New Foreign Key
    start_date = models.DateField()  #  Added
    end_date = models.DateField()    #  Added
    total_students = models.IntegerField()
    completed = models.BooleanField(default=False)  # New field to mark batch completion

    def __str__(self):
        status = " (Completed)" if self.completed else ""
        return f"{self.name} ({self.branch.name} - {self.course.name}){status}"





class ManagerProfile(Master):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="manager_user")
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Manager: {self.user.username}"

def student_photo_path(instance, filename):
    # print(instance)
    # print("hi")
    
    # Save photos directly in 'student_photos/' with student_id in filename
    ext = filename.split('.')[-1]  # Get file extension
    filename = f"{instance.student_id}.{ext}"  # Rename file as student_id.ext
    # print(filename)
    return os.path.join("student_photos", filename)

class SalesProfile(Master):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="sales_user")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    mobile_no = PhoneNumberField(null=True, blank=True, region='IN')  # 'IN' for India
    whatsapp_no = PhoneNumberField(null=True, blank=True, region='IN')
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="faculty_creator")
    reporting_officers = models.ManyToManyField(
        User,
        blank=True,
        related_name="sales_reporting_officers",
        help_text="Select reporting officers (Sales or Managers only)"
    )

    def clean(self):
        """Ensure only Sales/Manager users can be reporting officers."""
        # Skip M2M validation until the instance has a PK (unsaved instances can't use M2M safely)
        if not self.pk:
            return
        allowed_users = User.objects.filter(groups__name__in=['Sales', 'Manager']).distinct()
        invalid_officers = self.reporting_officers.exclude(id__in=allowed_users.values('id'))
        if invalid_officers.exists():
            raise ValidationError({
                'reporting_officers': f"Only Sales or Manager users can be reporting officers. Invalid users: {', '.join([u.username for u in invalid_officers])}"
            })

    def save(self, *args, **kwargs):
        """Force model validation before saving."""
        # self.full_clean()  # Runs `clean()` + field validations
        super().save(*args, **kwargs)
        # Need to call save again for ManyToMany relations
        # if 'reporting_officers' in kwargs:
        #     self.reporting_officers.set(kwargs['reporting_officers'])


    def __str__(self):
        # Avoid touching OneToOne descriptor before it's set; use *_id
        username = None
        if self.user_id:  # only safe to access when FK/OneToOne id is present
            try:
                username = self.user.username
            except Exception:
                username = None
        branch_name = None
        if self.branch_id:
            try:
                branch_name = self.branch.name
            except Exception:
                branch_name = None

        return f"{username or 'Unassigned'} ({branch_name or 'No Branch'})"

class StudentProfile(Master):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    # student_id = models.CharField(max_length=20, unique=True)
    # branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    # course = models.ForeignKey(Course, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    mobile_no = PhoneNumberField(null=True, blank=True, region='IN', unique=True)  # 'IN' for India
    whatsapp_no = PhoneNumberField(null=True, blank=True, region='IN', unique=True)
    sales_person = models.ForeignKey(
        SalesProfile,
        on_delete=models.CASCADE,  # mandatory, so CASCADE makes sense
        related_name="students",
        help_text="Select the counselor who enrolled this student"
    )
    drop_out = models.BooleanField(default=False, verbose_name="Drop Out")
    admission_date = models.DateField(
        help_text="Month & Year of admission"
    )
    dropout_date = models.DateField(null=True, blank=True,
        help_text="Dropped Out Date"
    )
    batch_change = models.BooleanField(null=True, blank=True, default=False, verbose_name="Batch Changed")
    batch_change_date = models.DateField(null=True, blank=True,
        help_text="Batch Changed Date"
    )
    placed = models.BooleanField(null=True, blank=True, default=False, verbose_name="Placed")
    placed_date = models.DateField(null=True, blank=True,
        help_text="Placed Date"
    )

    placement_pool_added = models.BooleanField(null=True, blank=True, default=False, verbose_name="Placement Pool Added")
    placement_pool_added_date = models.DateField(null=True, blank=True,
        help_text="Placement Pool Added Date"
    )

    def admission_month(self):
        return self.admission_date.month if self.admission_date else None

    def admission_year(self):
        return self.admission_date.year if self.admission_date else None
    
    def dropout_month(self):
        return self.dropout_date.month if self.dropout_date else None

    def dropout_year(self):
        return self.dropout_date.year if self.dropout_date else None

    def batch_change_month(self):
        return self.batch_change_date.month if self.batch_change_date else None

    def batch_change_year(self):
        return self.batch_change_date.year if self.batch_change_date else None
    
    def placed_month(self):
        return self.placed_date.month if self.placed_date else None

    def placed_year(self):
        return self.placed_date.year if self.placed_date else None
    # batch_changed = models.BooleanField(default=False, verbose_name="Batch Changed")
    # photo = models.ImageField(upload_to='student_photos/')
    # photo = models.ImageField(upload_to=student_photo_path)
    # last_updated = models.DateTimeField(auto_now=True)  # Automatically updated on save
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student_creator")

    def __str__(self):
        return f"{self.user.username}"

class PlacementProfile(Master):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="placement_user")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    mobile_no = PhoneNumberField(null=True, blank=True, region='IN')  # 'IN' for India
    whatsapp_no = PhoneNumberField(null=True, blank=True, region='IN')
    
    def __str__(self):
        return f"{self.user.username}"