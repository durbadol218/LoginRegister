from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm,UpdateUserForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse

from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.signing import Signer, BadSignature, SignatureExpired
# Create your views here.

def generate_activation_token(email):
    signer = Signer()
    return signer.sign(email)

def home(request):
    return render(request,'home.html')

def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=True)
                user.is_active = False #By default
                user.save()
                
                user_token = generate_activation_token(user.email)
                user_activation_link = request.build_absolute_uri(reverse('activate', args=[user_token]))
                
                messages.success(request, 'Congratulations! Please check your email to activate your account.')
                mail_subject = "Confirm Your Account"
                message = render_to_string('activation_email.html', {
                    'user': user,
                    'user_activation_link': user_activation_link
                })
                to_email = user.email
                print(to_email)
                email = EmailMultiAlternatives(mail_subject, '', to=[to_email])
                email.attach_alternative(message, "text/html")
                email.send()
                return redirect('login')
            else:
                messages.error(request, 'Please provide a valid information.')
        else:
            form = RegisterForm()
        return render(request, './signup.html',{'form':form})
    else:
        return redirect('profile')
    # else:
    #     return redirect('profile')
                
                
    #             messages.success(request, 'Congratulations! Account created successfully!')
    #             mail_subject = "Welcome to Our Website!"
    #             message = render_to_string('email.html', {
    #                 'user': user
    #             })
    #             to_email = user.email
    #             print(to_email)
    #             email = EmailMultiAlternatives(mail_subject, '', to=[to_email])
    #             email.attach_alternative(message, "text/html")
    #             email.send()
    #             # print(form.cleaned_data)
    #             return redirect('profile')
    #         else:
    #             messages.error(request, 'Please provide valid information!')
    #     else:
    #         form = RegisterForm()
    #     return render(request, './signup.html',{'form':form})

def activate(request,token):
    signer = Signer()
    try:
        email = signer.unsign(token)
        user = get_object_or_404(User, email=email)
        user.is_active = True
        user.save()
        
        messages.success(request, 'Welcome! Your account activated successfully!')
        mail_subject = "Welcome to Our Website!"
        message = render_to_string('email.html', {
            'user': user
        })
        to_email = user.email
        print(to_email)
        email = EmailMultiAlternatives(mail_subject, '', to=[to_email])
        email.attach_alternative(message, "text/html")
        email.send()
        # print(form.cleaned_data)
        return redirect('profile')
    except (BadSignature, SignatureExpired):
        messages.error(request, 'The activation link is invalid or has expired.')
        return redirect('login')
    
def userLogin(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request,data = request.POST)
            if form.is_valid():
                name = form.cleaned_data['username']
                userpass = form.cleaned_data['password']
                user = authenticate(username = name, password=userpass) # check kortesi user ase kina!
                if user is not None:
                    login(request,user)
                    messages.success(request, 'User login successful!')
                    return redirect('profile')
                else:
                    messages.error(request, 'User not found!')
            else:
                messages.error(request, 'Invalid username or password!')
        else:
            form = AuthenticationForm()
        return render(request, './login.html',{'form':form})
    else:
        return redirect('profile')
    
def userLogout(request):
    logout(request)
    messages.success(request, 'User logged out successfully!')
    return redirect('login')
        

def profile(request):
    if request.user.is_authenticated:
        return render(request, './profile.html',{'user':request.user})
    else:
        messages.error(request, 'You have need to login first!')
        return redirect('login')

@login_required(login_url='login') #only users can change his/her password!
def changePassword(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form = PasswordChangeForm(user=request.user, data = request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Your password has been changed successfully(with old password)!')
                return redirect('profile')
        else:
            form = PasswordChangeForm(user=request.user)
        return render(request,'./passchange.html',{'form':form})
    else:
        return redirect('login')
    
@login_required(login_url='login')
def updateUser(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UpdateUserForm(request.POST,instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your profile updated successfully!')
                print(form.cleaned_data)
                return redirect('profile')
            else:
                messages.error(request, 'Sorry,Your profile was not updated!')
        else:
            form = UpdateUserForm(instance=request.user)
        return render(request,'./updateUser.html',{'form':form})
    else:
        redirect('signup')

@login_required(login_url='login') #only users can change his/her password!
def setPassword(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form = SetPasswordForm(user=request.user, data = request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Your password has been changed successfully!')
                return redirect('profile')
        else:
            form = SetPasswordForm(user=request.user)
        return render(request,'./passchange.html',{'form':form})
    else:
        return redirect('login')

# from django.contrib.auth.views import PasswordResetView

# class CustomPasswordResetView(PasswordResetView):
#     html_email_template_name = 'registration/password_reset_email.html'