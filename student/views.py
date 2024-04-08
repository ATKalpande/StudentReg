from django.shortcuts import render,redirect
from .forms import StudForm,SForm
from .models import  stud
from django.contrib.auth import authenticate,login

from django.contrib.auth import logout
from django.contrib.auth.forms  import UserCreationForm,AuthenticationForm


def home(request):
    return render(request,"home.html")

def signup(request):
    if request.user.is_authenticated:
        return redirect('/base')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/base')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect the user to the desired page upon successful login
                return redirect('/base')  # Replace '/base' with the URL you want to redirect to
            else:
                msg = 'Invalid username or password'
        else:
            msg = 'Invalid input'
    else:
        form = AuthenticationForm()
        msg = ''
    return render(request, 'login.html', {'form': form, 'msg': msg})

def signout(request):
    logout(request)
    return redirect('/')

def base(request):
    return render(request,"base.html")



# View for student registration
def registerStd(request):
    title = "New Student Registration"
    form = StudForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data["s_name"]
            classN = form.cleaned_data["s_class"]
            add = form.cleaned_data["s_add"]
            email = form.cleaned_data["s_email"]
            
            # Check if the email already exists in the database
            if stud.objects.filter(s_email=email).exists():
                return render(request, 'ack.html', {"title": "Student Already Exists"})
            else:
                p = stud(s_name=name, s_class=classN, s_add=add, s_email=email)
                p.save()
                return render(request, 'ack.html', {"title": "Registered Successfully"})
    
    context = {
        "title": title,
        "form": form
    }
    
    return render(request, 'registerStd.html', context)

# View for listing all registered students
def existsStd(request):
    title = "All Registered Students"
    queryset = stud.objects.all()
    
    context = {
        "title": title,
        "queryset": queryset
    }
    
    return render(request, "existing.html", context)

# View for searching for a student
def search(request):
    title = "Search Student"
    form = SForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data['s_name']
            queryset = stud.objects.filter(s_name__icontains=name) # Case-insensitive search
            
            context = {
                'title': title,
                'queryset': queryset,
            }
            return render(request, 'existing.html', context)
    
    context = {
        'title': title,
        'form': form,
    }
    
    return render(request, 'search.html', context)
def dropout(request):
    title = "Student Removed Succesfully"
    form = SForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data['s_name']
            # Find the student by name
            student = stud.objects.filter(s_name=name).first()
            if student:
                # Delete the student if found
                student.delete()
                # Redirect to the same page with a success message
                return redirect('dropout') 
            else:
                return render(request, 'dropout.html', {'title': title, 'form': form, 'error_message': 'Student not found'})
    
    context = {
        'title': title,
        'form': form,
    }
    
    return render(request, 'dropout.html', context)