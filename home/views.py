
from django.shortcuts import render , HttpResponse
from home.models import contact
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate , login , logout
from first import settings
from django.core.mail import send_mail , EmailMessage
from . tokens import generate_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
# Create your views here.
def hom (request):
    context = {'success' : False}
    return render(request , 'home.html' , context)

def ord (request):
    return render(request , 'order.html')

def ive (request):
    return render(request , 'Indian-Veg.html')

def inv (request):
    return render(request , 'Indian-Non-Veg.html')

def chi (request):
    return render(request , 'Chinese.html')

def spe (request):
    return render(request , 'Special.html')

def Contact(request):
    context = {'success' : False , 'disp' : False}
    
    if request.method=="POST":
        context = {'success' : False , 'disp' : True}
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
       
        if len(name) == 0 :
            return render(request , 'contact.html' , context)
        if len(email) == 0 :
            return render(request , 'contact.html' , context)
        if len(phone) != 10 :
            return render(request , 'contact.html' , context)

        ins = contact(name = 'name' , email = 'email' , phone= 'phone')
        context = {'success' : True , 'disp' : True}
        ins.save()
       

    return render(request , 'contact.html' , context)

def signin(request):
    context = {'success' : False}
     
    if request.method == "POST" :
        
        username = request.POST['username']
        pass1 = request.POST['pass1']
        user = authenticate(username = username , password = pass1)
        context = {'success' : True , 'username' : username}    
        
        if user is not None :
            login(request , user)
            return render(request , "home.html" , context )
        else :
            return render(request , 'signin.html' , context)
        
    return render(request , 'signin.html')    
    

def signup(request):

    if request.method == "POST" :
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        email =request.POST['email']
        address = request.POST['address']

        myuser = User.objects.create_user(username=username , email=email , password= pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.address = address 
        myuser.is_active = False
        myuser.save()

        messages.success(request , "Successfully registered")
        
        # Welcome Email
        subject = "Welcome to our Food Website"
        message = "Hello, Hope you are good and healthy" + myuser.username + "!" + "Thank you for adding us to your basket!"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject=subject ,message= message ,from_email= from_email ,recipient_list= to_list , fail_silently = False)

         # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ GFG - Django Login!!"
        message2 = render_to_string('email_confirmation.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = False
        email.send()

        return redirect('signin')
    return render(request , 'signup.html')

def signout(request) :
    context = {'log' : False}
    if request.method == "POST" :
        logout(request)
        context = {'log' : True}
        return render(request , 'signin.html' , context)
    
def activate(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')
