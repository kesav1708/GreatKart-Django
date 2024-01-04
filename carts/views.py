from django.shortcuts import render,redirect
from store.models import Product,Variation
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


# Create your views here.

## Getting Cart id from session key

def _cart_id(request): ## private func
  cart=request.session.session_key ## get the session key
  if not cart:
    cart=request.session.create() ## creating the session key
  return cart



def add_cart(request,product_id):

  current_user = request.user

  ## Getting Product
  product=Product.objects.get(id=product_id) 

  ## If User is Authenticated..
  if current_user.is_authenticated:

    ## Getting Product Variations List.
    product_variation=[]

    if request.method == 'POST':
      for item in request.POST:
        key = item    ##  (Ex : color and size)
        value = request.POST[key]  ## (Ex : Blue and Medium)

        try:
          ## Getting Product Variation
          variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
          product_variation.append(variation)

        except:
          pass


    ## Getting CartItem
    is_cart_item_exists=CartItem.objects.filter(product=product,user=current_user).exists()

    if is_cart_item_exists:
      cart_item=CartItem.objects.filter(product=product,user=current_user)

      # Getting the Existing Variation List.
      existing_variation_list=[]
      id=[]

      for item in cart_item:
        existing_variation = item.variations.all()
        existing_variation_list.append(list(existing_variation))
        id.append(item.id)

      if product_variation in existing_variation_list:

        ### gives the position 
        index=existing_variation_list.index(product_variation)

        ### Getting Item id
        item_id=id[index]

        ### Getting Item
        item=CartItem.objects.get(product=product,id=item_id)

        ### Increase the Cart Quantity
        item.quantity +=1
        item.save()

      else:
        item=CartItem.objects.create(product=product,quantity=1,user=current_user)
        if len(product_variation) > 0:
          item.variations.clear()
          item.variations.add(*product_variation)
        item.save()

    else :
      cart_item=CartItem.objects.create(
        product=product,
        user=current_user,
        quantity =1,
      )

      if len(product_variation) > 0:
        cart_item.variations.clear()
        cart_item.variations.add(*product_variation)
      cart_item.save()

    return redirect('cart')



  

  ## If User is Not  Authenticated..
  else:

    ## Getting product_variation List.
    product_variation=[]

    if request.method == 'POST':
      for item in request.POST:
        key = item    ##  (Ex : color and size)
        value = request.POST[key]  ## (Ex : Blue and Medium)

        try:
          ## Getting Product Variation
          variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
          product_variation.append(variation)

        except:
          pass


    ## Getting Cart
    try:
      cart=Cart.objects.get(cart_id=_cart_id(request)) ## get the cart using cart_id present in session
    except Cart.DoesNotExist:
      cart=Cart.objects.create(
        cart_id=_cart_id(request)
        )
    cart.save()

    ## Getting CartItem
    is_cart_item_exists=CartItem.objects.filter(product=product,cart=cart).exists()
    if is_cart_item_exists:
      cart_item=CartItem.objects.filter(product=product,cart=cart)

      # Getting the Existing Variation List.
      existing_variation_list=[]
      id=[]

      for item in cart_item:
        existing_variation = item.variations.all()
        existing_variation_list.append(list(existing_variation))
        id.append(item.id)

      if product_variation in existing_variation_list:

        ### gives the position 
        index=existing_variation_list.index(product_variation)

        ## Getting item 
        item_id=id[index]
        item=CartItem.objects.get(product=product,id=item_id)

        ### Increase the Cart Quantity
        item.quantity +=1
        item.save()

      else:
        item=CartItem.objects.create(product=product,quantity=1,cart=cart)
        if len(product_variation) > 0:
          item.variations.clear()
          item.variations.add(*product_variation)
        item.save()

    else :
      cart_item=CartItem.objects.create(
        product=product,
        cart=cart,
        quantity =1,
      )

      if len(product_variation) > 0:
        cart_item.variations.clear()
        cart_item.variations.add(*product_variation)
      cart_item.save()

    return redirect('cart')


def remove_cart(request,product_id,cart_item_id):

  product=Product.objects.get(id=product_id)

  try:
    if request.user.is_authenticated:
      cart_item = CartItem.objects.get(product=product,user=request.user,id=cart_item_id)

    else:
      cart=Cart.objects.get(cart_id =_cart_id(request))
      cart_item = CartItem.objects.get(product=product,cart=cart,id=cart_item_id)

    if cart_item.quantity > 1:
      cart_item.quantity -= 1
      cart_item.save()
      
    else:
      cart_item.delete()

  except:
    pass

  return redirect('cart')


def remove_cart_item(request,product_id,cart_item_id):

  product=Product.objects.get(id=product_id)
  if request.user.is_authenticated:
    cart_item = CartItem.objects.get(product=product,user=request.user,id=cart_item_id)

  else:
    cart=Cart.objects.get(cart_id =_cart_id(request))
    cart_item = CartItem.objects.get(product=product,cart=cart,id=cart_item_id)

  cart_item.delete()
  return redirect('cart')


def cart(request,total=0,quantity=0,cart_items=None):
  try:
    tax=0
    grand_total=0

    if request.user.is_authenticated:
      ## If user logged in , Getting the Cartitems for the user.
      cart_items=CartItem.objects.filter(user=request.user,is_active=True)

    else:
      cart=Cart.objects.get(cart_id=_cart_id(request))
      cart_items=CartItem.objects.filter(cart=cart,is_active=True)

    for cart_item in cart_items:
      total +=(cart_item.product.price * cart_item.quantity)
      quantity += cart_item.quantity

    tax =(3 * total)/100
   
    grand_total = total + tax


  except ObjectDoesNotExist:
    pass

  context={
    'total' : total,
    'quantity' : quantity,
    'cart_items' : cart_items,
    'tax': tax,
    'grand_total': grand_total,
    
  }


  return render(request,'store/cart.html',context)


### Force User to Login When User move to Checkout

@login_required(login_url = 'login')
def checkout(request,total=0,quantity=0,cart_items=None):

  try:
    
    tax=0
    grand_total=0


    if request.user.is_authenticated:
      ## If user logged in , Getting the Cartitems for the user.
      cart_items=CartItem.objects.filter(user=request.user,is_active=True)

    else:
      cart=Cart.objects.get(cart_id=_cart_id(request))
      cart_items=CartItem.objects.filter(cart=cart,is_active=True)

    for cart_item in cart_items:
      total +=(cart_item.product.price * cart_item.quantity)
      quantity += cart_item.quantity

    tax =(3 * total)/100
   
    grand_total = total + tax


  except ObjectDoesNotExist:
    pass

  context={
    'total' : total,
    'quantity' : quantity,
    'cart_items' : cart_items,
    'tax': tax,
    'grand_total': grand_total,
    
  }

  return render(request,'store/checkout.html',context)


