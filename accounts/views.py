from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from .models import Account

# Verification Email Imports
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


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
            # messages.success(request, "You have signed up successfully.")
            # return redirect('sign_up')
        
        
            # Sending Account Activation Mail
            # Get the current site domain
            current_site = get_current_site(request)
            # Your activation email subject is
            mail_subject = 'TechLoad account activation'
            # Render your email message to string here or 
            # add the html file contains your message if exists
            message = render_to_string('accounts/account-verification-email.html', {
                # Return the user object
                'user': user,
                # Return the current site
                'domain': current_site,
                # Encode or Encrypt User id or pk
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # Creating new token for this particular user using the default token generator.
                'token': default_token_generator.make_token(user),
            })
            # After collecting these data and 
            # creating token start sending the email
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            # messages.success(request, F'Thanks for your registration <strong>{first_name}</strong>, </br> We have sent you an activation email,please go to your email inbox <strong>{to_email}</strong> and click on \
            # received activation link to confirm and complete your registration. </br> <strong>Note:</strong> Check your spam folder.')

            return redirect('/accounts/register/?command=verification&email='+email)

    # If form has no data to POST, return the registration form
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Congratulations! Your account has been activated')
        return redirect('sign_in')

    else:
        messages.error(request, 'Invalid activation link')
        return redirect('sign_up')



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
            return redirect('profile_info')
        
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



# Login decorator to make sure that user is logged in 
# if not logged in go back to login page
@login_required(login_url='sign_in')
# Profile Info View
def profileInfo(request):
    return render(request, 'accounts/profile-info.html')



# Profile Downloads View
@login_required(login_url='sign_in')
def profileDownloads(request):
    return render(request, 'accounts/profile-downloads.html')



# Profile Security View
@login_required(login_url='sign_in')
def profileSecurity(request):
    return render(request, 'accounts/profile-security.html')



# Profile Help Center View
@login_required(login_url='sign_in')
def profileHelpCenter(request):
    return render(request, 'accounts/profile-help-center.html')




# Profile Dashboard View
# @login_required(login_url='sign_in')
# def profileDashboard(request):
#     return render(request, 'accounts/profile-dashboard.html')


# Profile Notifications View
# @login_required(login_url='sign_in')
# def profileNotifications(request):
#     return render(request, 'accounts/profile-notifications.html')


# Profile Offers View
# @login_required(login_url='sign_in')
# def profileOffers(request):
#     return render(request, 'accounts/profile-offers.html')


# Profile Extended Offers View
# @login_required(login_url='sign_in')
# def profileExtendedOffers(request):
#     return render(request, 'accounts/profile-extended-offers.html')


# Profile Reviews View
# @login_required(login_url='sign_in')
# def profileReviews(request):
#     return render(request, 'accounts/profile-reviews.html')


# Profile Settings View
# @login_required(login_url='sign_in')
# def profileSettings(request):
#     return render(request, 'accounts/profile-settings.html')
