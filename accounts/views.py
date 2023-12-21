from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import Account
from carts.views import _cart_id
from carts.models import Cart,CartItem
from django.contrib import messages
from django.http import HttpResponse

### Login and Logout
from django.contrib import auth
from django.contrib.auth.decorators import login_required

## Verification Email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

import requests


# Create your views here.
def register(request):
  if request.method == 'POST':
    form=RegistrationForm(request.POST)
    if form.is_valid():
      ### Getting Values from Form
      first_name=form.cleaned_data['first_name']
      last_name=form.cleaned_data['last_name']
      phone_number=form.cleaned_data['phone_number']
      email=form.cleaned_data['email']
      password=form.cleaned_data['password']
      username=email.split('@')[0]

      ### Creating the User
      user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
      user.phone_number = phone_number
      user.save()

      ## USER ACTIVATION EMAIL
      current_site=get_current_site(request)
      mail_subject='Please Activate Your Account !'
      message=render_to_string('accounts/account_verification_email.html',{
        'user'   : user,
        'domain' : current_site,
        'uid'    : urlsafe_base64_encode(force_bytes(user.pk)),
        'token'  : default_token_generator.make_token(user),
      })

      to_email   = email
      send_email = EmailMessage(mail_subject, message, to=[to_email])
      send_email.send()
      
      return redirect('/accounts/login/?command=verification&email='+email)
    
  else:

    form=RegistrationForm()

  context={
    'form' : form,
  }

  return render(request,'accounts/register.html',context)

def login(request):
  if request.method == 'POST':
    email=request.POST['email']
    password=request.POST['password']

    user = auth.authenticate(email=email,password=password)
    if user is not None:
      ## Checking for Any Cart When user logged In..
      try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        
        ## Checking Whether the Cart exists or not
        is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()

        if is_cart_item_exists:
          ## Getting the Cart id
          cart_item=CartItem.objects.filter(cart=cart)

          ## Getting the Product Variation List.
          product_variation=[]
          for item in cart_item:
            variation = item.variations.all()
            product_variation.append(list(variation))


          ## Getting the Existing Variation List.
            
          cart_item=CartItem.objects.filter(user=user)
          existing_variation_list=[]
          id=[]

          for item in cart_item:
            existing_variation = item.variations.all()
            existing_variation_list.append(list(existing_variation))
            id.append(item.id)


          ## Getting the Comman Product Variations in both product and existing variation lists.
          
          for pr in product_variation:
            if pr in existing_variation_list:

              ### gives the position where we find the command item
              index = existing_variation_list.index(pr)

              item_id = id[index]
              item = CartItem.objects.get(id=item_id)
              item.quantity += 1
              item.user = user
              item.save()

            else:

              cart_item = CartItem.objects.filter(cart=cart)
              ## Assigning User for Each items in the cartitems
              for item in cart_item:
                item.user = user
                item.save()


      except:
        pass


      auth.login(request, user)
      messages.success(request,'You Are Now Logged In')

      ### It will Grab the  Previous Url 
      url = request.META.get('HTTP_REFERER')
      try:
        ## Getting Previous url (next=/cart/checkout/)
        query=requests.utils.urlparse(url).query

        ## It gives dict as {'next' : '/cart/checkout/'}
        params = dict(x.split('=') for x in query.split('&'))
        if 'next' in params:
          nextPage = params['next']
          return redirect(nextPage)

      except:
        return redirect('dashboard')

      

    else:
      messages.error(request,'Invalid Login Credentials')
      return redirect('login')
      


  return render(request,'accounts/login.html')

 

### It should be Accessed  only When You are Logged in.
@login_required(login_url = 'login')

def logout(request):
  auth.logout(request)
  messages.success(request,'You Are Logged Out')
  return redirect('login')


def activate(request, uidb64, token):
  try:
    ## Gives Primary Key of the User
    uid = urlsafe_base64_decode(uidb64).decode()

    ## Return User Object
    user = Account._default_manager.get(id=uid)

  except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
    user = None
  
  ## Check the Token Whether it is Secure Request or Not
  if user is not None and default_token_generator.check_token(user, token):
    user.is_active  = True
    user.save()
    messages.success(request,'Congratulations! Your Account is Activated.')
    return redirect('login')
  
  else:
    messages.error(request,'Invalid Activation Link')
    return redirect('register')
  

### It should be Accessed  only When You are Logged in.
@login_required(login_url = 'login')

def dashboard(request):
  return render(request,'accounts/dashboard.html')


def forgotpassword(request):
  if request.method ==  'POST':
    ## Getting Email
    email = request.POST['email']
    ## Checking Whether email is existing or not 
    if Account.objects.filter(email=email).exists():

      ## Getting User from email
      user = Account.objects.get(email__exact=email)

      ## RESET PASSWORD ACTIVATION EMAIL

      current_site=get_current_site(request)
      mail_subject='Reset Your Password'
      message=render_to_string('accounts/reset_password_email.html',{
        'user'   : user,
        'domain' : current_site,
        'uid'    : urlsafe_base64_encode(force_bytes(user.pk)),
        'token'  : default_token_generator.make_token(user),
      })

      to_email   = email
      send_email = EmailMessage(mail_subject, message, to=[to_email])
      send_email.send()

      messages.success(request,'Password Reset Email has been send to Your Email Address')
      return redirect('login')

    else:
      messages.error(request,'Account Does Not Exist')
      return redirect('forgotpassword')


  return render(request,'accounts/forgotpassword.html')


def resetpassword_validate(request,uidb64,token):
  try:
    ## Gives Primary Key of the User
    uid = urlsafe_base64_decode(uidb64).decode()

    ## Return User Object
    user = Account._default_manager.get(id=uid)

  except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
    user = None

  ## Check the Token Whether it is Secure Request or Not
  if user is not None and default_token_generator.check_token(user, token):

    ### Saving the uid in the session.
    request.session['uid'] = uid

    messages.success(request,'Please Reset Your Password')
    return redirect('resetpassword')
  
  else:
    messages.error(request,'This Link has been Expired.')
    return redirect('login')


def resetpassword(request):
  if request.method == 'POST':
    password=request.POST['password']
    confirm_password=request.POST['confirm_password']

    if password == confirm_password:
      ## Getting uid from the session
      uid = request.session.get('uid')

      ## Get User
      user = Account.objects.get(pk=uid)
      user.set_password(password)
      user.save()
      messages.success(request,'Password Reset Successfull')
      return redirect('login')


    else:
      messages.error(request,'Password does not match.')
      return redirect('resetpassword')
    

    
  else:
    return render(request,'accounts/resetpassword.html')

