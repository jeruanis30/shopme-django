from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

#verification Email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


from django.http import HttpResponse

# Create your views here.

def register(request):
    if request.method == 'POST':
        #form will hold all the data
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0]

            #added functionality
            user = Account.objects.all()
            username_list =[]
            for n in user:
                username_list.append(n.username)
            for uname in username_list:
                if username == uname:
                    username = username + str(-3)
                    num = username.split('-')[1]
                    ustring = username.split('-')[0]
                    conv_num = int(num)
                    num = conv_num+1
                    username = ustring+'-'+str(num)

                else:
                    username == username
            #end added functionality

            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password, username=username)
            user.phone_number=phone_number
            user.save()

            #USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user':user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            #useractivation end

            # messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email address. Please verify it')
            return redirect('/accounts/login?command=verification&email='+email)
    else:
        form = RegistrationForm()

    context= {'form':form}
    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user=auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now loggedin.')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Username or Password is incorrect!')
            return redirect('login')
    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.info(request, 'logout successful')
    return redirect('login') #this does not need logout template

def activate(request, uidb64, token):
    #decode the ids
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is now active.')
        return redirect('login')
    else:
        messages.warning(request, 'Invalid activation link')
        return redirect('register')

def forgotPasswordResetValidate(request, uidb64, token):
        #decode the ids
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = Account._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
            user=None

        if user is not None and default_token_generator.check_token(user, token):
            request.session['uid'] = uid
            messages.success(request, 'Please reset your password')
            return redirect('forgotPasswordReset_page')
        else:
            messages.warning(request, 'This link has been expired')
            return redirect('login')

def forgotPasswordReset_page(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful, login below.')
            return redirect('login')
        else:
            messages.warning(request, 'Password do not match.')
            return redirect('forgotPasswordReset_page')
    else:
        return render(request, 'accounts/forgotPasswordReset_page.html')

@login_required(login_url = 'login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            #RESET PASSWRD EMAIL
            current_site = get_current_site(request)
            mail_subject = 'Reset Password'
            message = render_to_string('accounts/forgotPassword_verification_email.html', {
                'user':user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            #useractivation end
            # messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('/accounts/login?command=pwdvalidation&email='+email)
        else:
            messages.warning(request, 'Account does not exists.')
            return redirect('forgotPassword')

    return render(request, 'accounts/forgotPassword.html')
