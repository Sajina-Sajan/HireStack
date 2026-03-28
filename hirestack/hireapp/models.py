from django.db import models 

from django.contrib.auth.models import User




# class Account(models.Model):
#     ROLE_CHOICES = (
#         ('user', 'User'),
#         ('employee', 'Employee'),
#         ('admin', 'Admin'),
#     )

#     username = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES)

#     def __str__(self):
#         return self.username

class JobPortalUser(models.Model):
    ROLE_CHOICES = [
        ('junior_dev', 'Junior Developer'),
        ('mid_dev', 'Mid-Level Developer'),
        ('senior_dev', 'Senior Developer'),
        ('lead_dev', 'Lead Developer'),
        ('architect', 'Architect / Principal Developer'),
    ]

    full_name = models.CharField(max_length=255)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user',
    )
    
    phone_number = models.CharField(max_length=10 , blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    location = models.CharField(max_length=255, blank=True)
    college_name = models.CharField(max_length=255, blank=True)
    degree = models.CharField(max_length=100, blank=True)
    year_of_study = models.CharField(max_length=50, blank=True)
    about_me = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

    
class Experience(models.Model):
    user = models.ForeignKey(
        JobPortalUser,
        on_delete=models.CASCADE,
        related_name='experiences'
    )

    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)

    description = models.TextField()

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.job_title} - {self.company_name}"
    


class JobPortalEmployee(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    employee_id= models.CharField(max_length=128) 
    department = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128) 
    is_blocked = models.BooleanField(default=False)



    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    

class JobPost(models.Model):
    JOB_TYPE_CHOICES = [
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]
    employee = models.ForeignKey(
        JobPortalEmployee,
        on_delete=models.CASCADE,
        related_name="jobs"
    )


    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)

    
    location = models.CharField(max_length=255, blank=True)
    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPE_CHOICES,
        default='full-time'
    )
    salary = models.CharField(max_length=100, blank=True)

    
    required_skills = models.TextField(
        help_text="Comma separated skills (e.g. Python, Django, AWS)",
        blank=True
    )
    description = models.TextField()

    
    apply_url = models.CharField(
        max_length=500,
        blank=True,
        help_text="External apply link or contact email"
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def skills_list(self):
        if not self.required_skills:
            return []
        return [skill.strip() for skill in self.required_skills.split(',') if skill.strip()]

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"
    

class JobApplication(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(JobPortalUser, on_delete=models.CASCADE)

    job = models.ForeignKey(
        JobPost,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    cover_letter = models.TextField(blank=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    is_blocked = models.BooleanField(default=False)

    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} -> {self.job.job_title}"
    


class MockTest(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.job.job_title}"
    
class Question(models.Model):
    test = models.ForeignKey(MockTest, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct = models.IntegerField()  # 1-4

    def __str__(self):
        return self.question
    
class TestResult(models.Model):
    user = models.ForeignKey(JobPortalUser, on_delete=models.CASCADE)
    test = models.ForeignKey(MockTest, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.test.title}"

    @property
    def percentage(self):
        if self.total:
            return round((self.score / self.total) * 100)
        return 0



