from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from .models import Account

# Create your views here.


def register(request):
    # Making sure form method is POST
    if request.method == 'POST':
        
        # Requesting all the form posted data
        form = RegistrationForm(request.POST)
        
        # Making sure form data is valid
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            gender = form.cleaned_data['gender']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Create User Account using the Account Manager func create_user
            user = Account.objects.create_user(first_name=first_name, last_name=last_name,
                    gender=gender, phone_number=phone_number, email=email, password=password)
            
            # Save the new user data to the account model
            user.save()
            
            # Successful Registration Message
            messages.success(request, "You have signed up successfully.")
            return redirect('sign_up')

    # If form has no data to POST, return the registration form
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)



def login(request):
    # Making sure form method is POST
    if request.method == 'POST':
        
        # Requesting the form input fields named 'email' & 'password'  
        email = request.POST['email']
        password = request.POST['password']
        
        # Return the User object to check if the form 
        # inputs are the same as user's email and password
        user = auth.authenticate(email=email, password=password)
        
        # If User Exists
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You have signed in successfully.')
            return redirect('home')
        
        # If User Doesn't Exists
        else:
            messages.error(request, 'Invalid login credintials!')
            return redirect('sign_in')
        
    return render(request, 'accounts/login.html')




# Login decorator to make sure that user 
# is logged in to view this page
@login_required(login_url='sign_in')
# LogOut View
def logout(request):
    # Return the User object to logout him or her
    auth.logout(request)
    messages.success(request, 'You have signed out successfully. Come back soon!')
    return redirect('sign_in')



# Profile Info View
# Login decorator to make sure that user is logged in 
# if not logged in go back to login page
@login_required(login_url='sign_in')
def profileDashboard(request):
    return render(request, 'accounts/profile-dashboard.html')
