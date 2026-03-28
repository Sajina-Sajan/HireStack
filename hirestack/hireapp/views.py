from django.shortcuts import render, redirect , get_object_or_404
from django.contrib import messages  
from .models import JobPortalUser 
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect
from .models import JobPortalEmployee
from .models import Experience
from .models import JobPost
from .models import JobApplication
from .models import MockTest
from .models import TestResult
from .models import Question
from django.contrib.auth.models import User 
from django.utils.dateparse import parse_datetime
from django.db.models import Exists, OuterRef
# from .models import Account




# def login_view(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']

#         try:
#             user = Account.objects.get(username=username, password=password)

#             request.session['user_id'] = user.id

#             if user.role == 'user':
#                 return redirect('home')  

#             elif user.role == 'employee':
#                 return redirect('emland')  

#             elif user.role == 'adminn':
#                 return redirect('admindash')  

#         except Account.DoesNotExist:
#             return render(request, "login.html", {"error": "Invalid credentials"})

#     return render(request, "login.html")




def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        role = request.POST.get('role', 'user')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        password = request.POST.get('password')
        location = request.POST.get('location')
        college_name = request.POST.get('college_name')
        degree = request.POST.get('degree')
        year_of_study = request.POST.get('year_of_study')
        about_me = request.POST.get('about_me')
        skills = request.POST.get('skills')
        resume = request.FILES.get('resume')

        
        if JobPortalUser.objects.filter(full_name=full_name).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'register.html')
        
        
        
        
        if JobPortalUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'register.html')

        
       


        JobPortalUser.objects.create(
            full_name=full_name,
            role=role,
            email=email,
            password=password,
            phone_number=phone_number,
            location=location,
            college_name=college_name,
            degree=degree,
            year_of_study=year_of_study,
            about_me=about_me,
            skills=skills,
            resume=resume
        )

        messages.success(request, 'Registration successful!')
        return redirect('landing')

    return render(request, 'register.html')



def loginn(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = JobPortalUser.objects.get(email=email)
        except JobPortalUser.DoesNotExist:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')

        if user is not None and (password==user.password):
            request.session['user_id'] = user.id
            messages.success(request, f'Welcome, {user.email}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')





def home(request):
    if 'user_id' not in request.session:
        return redirect('login')

    user_id = request.session['user_id']
    user = JobPortalUser.objects.get(id=user_id)

    has_applied_subquery = JobApplication.objects.filter(
        job=OuterRef('pk'),
        user=user
    )

    jobs = JobPost.objects.filter(is_active=True)\
        .annotate(has_applied=Exists(has_applied_subquery))\
        .order_by('-created_at')

    notifications = JobApplication.objects.filter(user=user)\
        .exclude(status='pending')\
        .order_by('-applied_at')

    
    # Get all test IDs the user has already attended
    attended_test_ids = TestResult.objects.filter(user=user).values_list('test_id', flat=True)

    # Fetch mock tests that the user HAS NOT attended yet
    available_mock_tests = MockTest.objects.exclude(id__in=attended_test_ids).order_by('-created_at')

    return render(request, 'home.html', {
        'jobs': jobs,
        'notifications': notifications,
        'available_mock_tests': available_mock_tests,   
    })



def adminlogin(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admindash')
        else:
            messages.error(request, "Invalid credentials or not authorized as admin")

    return render(request,'admin.html')


from django.db.models import Q
from .models import JobPortalUser, JobPortalEmployee, JobPost

def admindash(request):

    query = request.GET.get('q', '')

    users = JobPortalUser.objects.all()
    employees = JobPortalEmployee.objects.all()

    jobs = JobPost.objects.all()

    if query:
        jobs = JobPost.objects.filter(
            Q(job_title__icontains=query) |
            Q(location__icontains=query) |
            Q(company_name__icontains=query)
        )

    context = {
        "user_list": users,
        "people_list": employees,
        "job_list": jobs,
        "employee_count": employees.count(),
        "application_count": 0,
        "live_jobs_count": jobs.filter(is_active=True).count(),
    }

    return render(request, "admindash.html", context)

    

def about(request):
    return render(request,'about.html')




def job_view(request):
    # Generating "live" notifications for the demo
    notifications = [
        {
            'status': 'approved',
            'job': {'job_title': 'Frontend Developer'},
            # This creates a real time object 5 minutes ago
            'applied_at': datetime.now() - timedelta(minutes=5) 
        },
        {
            'status': 'rejected',
            'job': {'job_title': 'UI Designer'},
            # This creates a real time object 2 hours ago
            'applied_at': datetime.now() - timedelta(hours=2)
        }
    ]
    
    return render(request, 'your_template.html', {
        'notifications': notifications,
        'jobs': jobs_list 
    })


def dashboard(request):
    employee_id = request.session.get('employee_id')
    mock_test = None
    if employee_id:
        from hireapp.models import JobPortalEmployee
        try:
            employee = JobPortalEmployee.objects.get(id=employee_id)
            # Get the first mock test for this employee's jobs
            job = JobPost.objects.filter(employee=employee).first()
            if job:
                mock_test = MockTest.objects.filter(job=job).first()
        except JobPortalEmployee.DoesNotExist:
            pass

    return render(request, 'dashboard.html', {
        'mock_test': mock_test,
    })

def landingpage(request):
    return render(request,'landingpage.html')


# def users(request):
#     users = JobPortalUser.objects.order_by('full_name')
#     return render(request, 'users.html', {'users': users})

def block_user(request, user_id):
    user = JobPortalUser.objects.get(id=user_id)
    user.is_blocked = True
    user.save()
    return redirect('home')



def unblock_user( request, user_id):
    user = JobPortalUser.objects.get(id=user_id)
    user.is_blocked = False
    user.save()
    return redirect('home')


def emlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            employee = JobPortalEmployee.objects.get(email=email)
        except JobPortalEmployee.DoesNotExist:
            messages.error(request, 'Invalid username or password')
            return render(request, 'emlogin.html')

        if employee.password == password:
            request.session['employee_id'] = employee.id
            messages.success(request, 'Login successful')
            return redirect('dashboard')

        messages.error(request, 'Invalid username or password')

    return render(request, 'emlogin.html')



def emregister(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name  = request.POST.get('last_name')
        employee_id = request.POST.get('employee_id')
        department = request.POST.get('department')

        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if JobPortalEmployee.objects.filter(employee_id=employee_id).exists():
            messages.error(request, 'Employee ID already exists')
            return redirect('emregister')

        if JobPortalEmployee.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('emregister')
        
        print(f"Attempting to create employee: {email}")
        try:
            employee = JobPortalEmployee.objects.create(
                first_name=first_name,
                last_name=last_name,
                employee_id=employee_id,
                department=department,
                email=email,
                password=password
            )
            print(f"Employee created successfully: {employee.id}")
            messages.success(request,'Registration successful! Please log in.')
            return redirect('emland')
        except Exception as e:
            print(f"Error creating employee: {str(e)}")
            messages.error(request, f'Registration failed: {str(e)}')
            return redirect('emregister')

    return render(request,'emregister.html')



def userprofile(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    usep = JobPortalUser.objects.get(id=user_id)

    
    skills_list = usep.skills.split(',') if usep.skills else []
    exp = Experience.objects.filter(user=usep)
    test_history = TestResult.objects.filter(user=usep).select_related('test__job').order_by('-id')

    return render(request, 'userprofile.html', {
        'usep': usep,
        'skills_list': skills_list,
        'experiences': exp,
        'test_history': test_history,
    })










def addexp(request):
    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        company_name = request.POST.get('company_name')
        location = request.POST.get('location')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        description = request.POST.get('description')

        is_current = request.POST.get('is_current') == 'on'
        if is_current:
            end_date = None

        user_id = request.session.get('user_id')
        if not user_id:
            messages.error(request, "Please login first")
            return redirect('login')

        user = JobPortalUser.objects.get(id=user_id)

        Experience.objects.create(
            user=user,
            job_title=job_title,
            company_name=company_name,
            location=location,
            start_date=start_date,
            end_date=end_date,
            is_current=is_current,
            description=description
        )

        return redirect('userprofile')

    return render(request, 'addexp.html')









def jobposting(request):
    employee_id = request.session.get('employee_id')

    if not employee_id:
        return redirect('emlogin')

    employee = JobPortalEmployee.objects.get(id=employee_id)

    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        company_name=request.POST.get('company_name')
        location = request.POST.get('location')
        job_type = request.POST.get('job_type')
        salary = request.POST.get('salary')
        required_skills = request.POST.get('required_skills')
        description = request.POST.get('description')
        apply_url = request.POST.get('apply_url')

        if not job_title or not description:
            messages.error(request, "Job title and description are required.")
            return render(request, 'jobposting.html')

        JobPost.objects.create(
            employee=employee,
            job_title=job_title,
            company_name=company_name,  
            location=location,
            job_type=job_type,
            salary=salary,
            required_skills=required_skills,
            description=description,
            apply_url=apply_url
        )

        messages.success(request, "Job posted successfully")
        return redirect('emprofile')  

    return render(request, 'jobposting.html')




def logout_view(request):
    logout(request)
    return redirect('landing')

def emland(request):
    return render(request,'emland.html')

def logout_vieww(request):
    logout(request)
    return redirect('emland')


# def emprofile(request):
#     jobs = JobPost.objects.filter(posted_by=request.user).order_by('-created_at')
#     return render(request, 'emprofile.html', {'posted_jobs': jobs})


def emprofile(request):
    employee_id = request.session.get('employee_id')

    if not employee_id:
        return redirect('emlogin')

    employee = JobPortalEmployee.objects.get(id=employee_id)

    posted_jobs = JobPost.objects.filter(
        employee=employee
    ).prefetch_related('applications__user')

    for job in posted_jobs:
        mock_tests = MockTest.objects.filter(job=job)
        if mock_tests.exists():
            test = mock_tests.first()
            for app in job.applications.all():
                res = TestResult.objects.filter(user=app.user, test=test).first()
                if res:
                    app.test_score = res.score
                    app.test_total = res.total
                else:
                    app.test_score = None
                    app.test_total = None

    return render(request, 'emprofile.html', {
        'employee': employee,
        'posted_jobs': posted_jobs
    })

# def cv(request):
#     return render(request,'cv.html')



def apply_job(request, job_id):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = get_object_or_404(JobPortalUser, id=user_id)
    job = get_object_or_404(JobPost, id=job_id)

    # prevent duplicate applications
    if JobApplication.objects.filter(user=user, job=job).exists():
        messages.warning(request, "You already applied for this job")
        return redirect('home')

    JobApplication.objects.create(
        user=user,
        job=job,
        resume=user.resume if user.resume else None
    )

    messages.success(request, "Application submitted successfully!")
    return redirect('home')


def approve_application(request, app_id):
    employee_id = request.session.get('employee_id')
    if not employee_id:
        return redirect('emlogin')

    application = get_object_or_404(JobApplication, id=app_id)

    application.status = 'approved'
    application.save()

    messages.success(request, "Candidate approved")
    return redirect('emprofile')


def reject_application(request, app_id):
    employee_id = request.session.get('employee_id')
    if not employee_id:
        return redirect('emlogin')

    application = get_object_or_404(JobApplication, id=app_id)

    application.status = 'rejected'
    application.save()

    messages.warning(request, "Candidate rejected")
    return redirect('emprofile')


def create_test(request, job_id):
    job = JobPost.objects.get(id=job_id)

    if request.method == "POST":
        title = request.POST.get("title")
        test = MockTest.objects.create(job=job, title=title)
        return redirect('add_questions', test.id)

    return render(request, "create_test.html", {"job": job})

def add_questions(request, test_id):
    # Guard: only employees can access this
    employee_id = request.session.get('employee_id')
    if not employee_id:
        return redirect('emlogin')

    test = MockTest.objects.get(id=test_id)

    if request.method == "POST":

        for i in range(1, 16):
            question_text = request.POST.get(f'question_{i}')
            option1 = request.POST.get(f'o1_{i}')
            option2 = request.POST.get(f'o2_{i}')
            option3 = request.POST.get(f'o3_{i}')
            option4 = request.POST.get(f'o4_{i}')
            correct = request.POST.get(f'correct_{i}')

            if question_text:
                Question.objects.create(
                    test=test,
                    question=question_text,
                    option1=option1,
                    option2=option2,
                    option3=option3,
                    option4=option4,
                    correct=int(correct)
                )

        messages.success(request, 'Questions saved successfully!')
        return redirect('emprofile')

    return render(request, "add_questions.html", {
        "test": test,
        "range": list(range(1, 16))
    })

def attend_test(request, test_id):

    if 'user_id' not in request.session:
        return redirect('login')

    user = JobPortalUser.objects.get(id=request.session['user_id'])
    test = MockTest.objects.get(id=test_id)


    if TestResult.objects.filter(user=user, test=test).exists():
        messages.warning(request, "You already attended this test")
        return redirect('home')

    questions = test.questions.all()

    if request.method == "POST":
        score = 0
        total = questions.count()

        for q in questions:
            ans = request.POST.get(str(q.id))
            if ans and int(ans) == q.correct:
                score += 1

        result = TestResult.objects.create(
            user=user,
            test=test,
            score=score,
            total=total
        )

        return redirect('test_result', result.id)

    return render(request, "attend_test.html", {
        "test": test,
        "questions": questions,
    })

def test_result(request, result_id):
    if 'user_id' not in request.session:
        return redirect('login')

    result = get_object_or_404(TestResult, id=result_id)
    percentage = round((result.score / result.total) * 100) if result.total else 0
    # SVG dashoffset: circumference=276.46, filled portion = (1 - percentage/100) * 276.46
    dashoffset = round((1 - percentage / 100) * 276.46, 2)

    return render(request, 'test_result.html', {
        'test': result.test,
        'score': result.score,
        'total': result.total,
        'percentage': percentage,
        'dashoffset': dashoffset,
    })


def block_user(request, id):
    user = get_object_or_404(JobPortalUser, id=id)

    if user.is_blocked:
        user.is_blocked = False
    else:
        user.is_blocked = True

    user.save()
    return redirect('/admindash/#user-directory')


def block_employee(request, id):
    emp = get_object_or_404(JobPortalEmployee, id=id)

    if emp.is_blocked:
        emp.is_blocked = False
    else:
        emp.is_blocked = True

    emp.save()
    return redirect('/admindash/#employee-directory')


def delete_job(request, id):
    job = get_object_or_404(JobPost, id=id)
    job.delete()
    return redirect('/admindash/#job-postings')