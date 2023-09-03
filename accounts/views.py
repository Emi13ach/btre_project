from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.auth.models import User

def register(request):
    if request.method == "POST":
        # Get form values
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        
        # Check if passwords not match
        if password == password2:
            # Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, "That username is taken!")
                return redirect("register")
            # Check email
            elif User.objects.filter(email=email).exists():
                messages.error(request, "That email address is being used!")
                return redirect("register")
            else:
                # Validation is correct
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password
                    )
                user.save()
                messages.success(request, "You are now registered!")
                return redirect("login") 
        else:
            messages.error(request, "Passwords do not match!")
            return redirect("register")     
            
    else:
        return render(request, "accounts/register.html")

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in!")
            return redirect("dashboard")
        else:    
            messages.error(request, "Invalid credentials!")
            return redirect("login")
    else:
        return render(request, "accounts/login.html")

def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request, "You are logged out!")
        return redirect("index")

def dashboard(request):
    return render(request, "accounts/dashboard.html")

