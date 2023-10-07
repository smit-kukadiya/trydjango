from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from .seed import generate_report_card
from django.contrib.auth import get_user_model

User = get_user_model()

def home(request):
    return render(request, 'index.html', context={'page': 'Home Page'})

def person_detail(request):
    persons = [
        {'name': 'Smit', 'age': 21},
        {'name': 'Jack', 'age': 35}
    ]
    return render(request, 'person.html', context={'page': 'Person data', 'persons': persons})

@login_required(login_url='/login')
def add_person(request):
    if request.method == 'POST':
        data = request.POST
        name = data.get('name')
        age = data.get('age')
        photo = request.FILES.get('photo')
        print(name, age, photo)
        Person.objects.create(name= name, age=age, photo=photo)
        return redirect("/addPerson/")
    querySet = Person.objects.all()
    if request.GET.get('search'):
        querySet = querySet.filter(name__icontains = request.GET.get('search'))

    return render(request, 'add.html', context={'page': 'Add Person', 'persons': querySet})

def delete_person(request, id):
    querySet =  Person.objects.get(id=id)
    querySet.delete()
    return redirect("/addPerson/")

def update_person(request, id):
    querySet = Person.objects.get(id=id)
    if request.method == 'POST':
        data = request.POST
        name = data.get('name')
        age = data.get('age')
        photo = request.FILES.get('photo')
        print(name, age, photo)
        querySet.name = name
        querySet.age = age
        if photo:
            querySet.photo = photo
        querySet.save()
        return redirect("/addPerson/")
    return render(request, 'update.html', context={'page': 'Update Person', 'person': querySet})

def login_page(request):
    if request.method == 'POST':
        user_name = request.POST.get('userName')
        password = request.POST.get('pass')

        if not User.objects.filter(username = user_name).exists():
            messages.error(request, 'Invalid username')
            return redirect("/login/")
        
        user = authenticate(username= user_name, password=password)

        if user is None:
            messages.error(request, "Invalid password")
            return redirect("/login/")
        else:
            login(request, user)
            return redirect("/addPerson/")

    return render(request, 'login.html', context={'page': 'Login'})

def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        user_name = request.POST.get('userName')
        password = request.POST.get('pass')

        user = User.objects.filter(username = user_name)
        if user.exists():
            messages.info(request, "Username is exists.")
            return redirect("/register/")

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = user_name
        )
        user.set_password(password)
        user.save()
        messages.info(request, "Successfully register")
        return redirect('/login/')

    return render(request, 'register.html', context={'page': 'Register'})

def logout_page(request):
    logout(request)
    return redirect("/login/")

### New Student Report generator

def get_students(request):
    query = Student.objects.all()
    
    if request.GET.get('search'):
        search = request.GET.get('search')
        query = query.filter(
            Q(student_name__icontains=search) |
            Q(department__department__icontains=search) |
            Q(student_id__student_id__icontains=search) |
            Q(student_email__icontains=search) |
            Q(student_address__icontains=search)
        )

    paginator = Paginator(query, 10)  # Show 10 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'report/students.html', context={'page':'Student', 'page_obj':page_obj})

def see_marks(request, student_id):
    #generate_report_card()
    queryset = SubjectMarks.objects.filter(student__student_id__student_id = student_id)
    current_rank = ReportCard.objects.filter(student__student_id__student_id = student_id)
    total_marks = queryset.aggregate(total_marks= Sum('marks'))
    # i = 1
    # for rank in ranks:
    #     if student_id == rank.student_id.student_id:
    #         current_rank = i
    #         break
    #     i+=1
    return render(request, 'report/seeMarks.html', context={'queryset':queryset, 'total_marks':total_marks, 'current_rank': current_rank[0]})