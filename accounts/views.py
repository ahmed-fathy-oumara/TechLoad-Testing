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

# User Registration View
def register(request):
    # Making sure form method is POST
    if request.method == 'POST':
        
        # Requesting all the form posted data
        form = RegistrationForm(request.POST)
        
        # If you check all the below fields and form data is valid
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

            # Redirect the user to the register page and display the activation success email there
            # Pass the command verification email and the user email to the url and to the register page
            return redirect('/accounts/register/?command=verification&email='+email)

    # If form has no data to POST, return the registration form
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)



# User Activation View
# Pass the uidb and the token through the url to the view
def activate(request, uidb64, token):
    
    # Try Block: Try the below first
    try:
        # Decode or decrypt the id we encoded or encrypted in 
        # the above registration view and store it in uid variable
        uid = urlsafe_base64_decode(uidb64).decode()
        # Return the user object and store it in user
        user = Account._default_manager.get(pk=uid)
    
    # Except Block: Handling the errors we can meet during activation
    # If any of these errors happen set user to none and donot activate the account
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    # If user exists and the token is checked of this particular user
    if user is not None and default_token_generator.check_token(user, token):
        # Change user is_active status in database to true 
        user.is_active = True
        # Save user with the new active status
        user.save()

        # Send success message to the user that he activated the account
        messages.success(request, 'Congratulations! Your account has been activated')
        # Redirect user to the sign in page to login
        return redirect('sign_in')

    # Rather than that
    else:
        # Send error message
        messages.error(request, 'Invalid activation link')
        # Redirect user to the sign up page to register again
        return redirect('sign_up')


# User Login View
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



# User Forgot Password View
def forgotPassword(request):

    # If form method is POST
    if request.method == 'POST':
        # Get the inserted email and store it to the email
        email = request.POST['email']

        # Check if email exists in database
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__iexact=email)

            # Sending Reset Password Email
            # Get the current site domain
            current_site = get_current_site(request)
            # Your activation email subject is
            mail_subject = 'TechLoad Password Reset'
            # Render your email message to string here or
            # add the html file contains your message if exists
            message = render_to_string('accounts/reset-password-email.html', {
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

            # Display Reset Password Email Sent Success Message
            messages.success(request, 'Reset password email has been sent to your email.')
            # Redirect user to the sign in page to login with new password
            return redirect('sign_in')

        else:
            messages.error(request, 'This Account does not exist')
            return redirect('forgot_password')

    else:
        return render(request, 'accounts/forgot-password.html')

    

# Reset Password Validation Email View
# Pass the uidb and the token through the url to the view
def resetpassword_validate(request, uidb64, token):
    
    # Try Block: Try the below first
    try:
        # Decode or decrypt the id we encoded or encrypted in
        # the above forgot password view and store it in uid variable
        uid = urlsafe_base64_decode(uidb64).decode()
        # Return the user object and store it in user
        user = Account._default_manager.get(pk=uid)

    # Except Block: Handling the errors we can meet during resetting password
    # If any of these errors happen set user to none and donot reset the password
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    # If user exists and the token is checked of this particular user
    if user is not None and default_token_generator.check_token(user, token):
        # Save the uid inside the session to access this 
        # session later while reseting the password
        request.session['uid'] = uid

        # Display Reset Password Success Message
        messages.success(request, 'Please reset your password')
        return redirect('reset_password')

    # Display this message If user does not exist or 
    # used the link in the email after 1 hour or used old link
    else:
        messages.error(request, 'This link has been expired')
        return redirect('sign_in')



# Reset Password View
def resetPassword(request):
    
    # If form method is POST
    if request.method == 'POST':
        # Get the inserted input named password and store it to password
        password = request.POST['password']
        # Get the inserted input named confirm password and store it to confirm password
        confirm_password = request.POST['confirm_password']

        # If two password matches each other
        if password == confirm_password:
            # Get the uid from the session we saved above
            uid = request.session.get('uid')
            # Get the user account by id
            user = Account.objects.get(pk=uid)
            # Set the new password
            user.set_password(password)
            # Save user with new password in database
            user.save()

            # Display Reset Password Success Message
            messages.success(request, 'Your password has been reset successfully!')
            # Redirect user to sign in page to login with new password
            return redirect('sign_in')

        # Display Error Message If passwords donot match each other
        else:
            messages.error(request, 'Passwords do not match!')

    else:
        return render(request, 'accounts/reset-password.html')




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
