from django.shortcuts import render
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

    # If form has no data to POST, return the registration form
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    return render(request, 'accounts/login.html')


def logout(request):
    return render(request, 'accounts/logout.html')
