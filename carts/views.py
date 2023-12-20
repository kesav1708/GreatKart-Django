from django.shortcuts import render,redirect
from store.models import Product,Variation
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.


def _cart_id(request): ## private func
  cart=request.session.session_key ## get the session key
  if not cart:
    cart=request.session.create() ## creating the session key
  return cart

def add_cart(request,product_id):
  ## Getting Product
  product=Product.objects.get(id=product_id) 

  ## Getting Variations
  product_variation=[]

  if request.method == 'POST':
    for item in request.POST:
      key = item    ##  (Ex : color and size)
      value = request.POST[key]  ## (Ex : Blue and Medium)

      try:
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

    ### We need :
    ### Existing Variation ---> Coming from Database
    ### Current Variation  ---> Coming from Product Variation List
    ### Item_id ---> Coming from Database

    existing_variation_list=[]
    id=[]

    for item in cart_item:
      existing_variation = item.variations.all()
      existing_variation_list.append(list(existing_variation))
      id.append(item.id)

    if product_variation in existing_variation_list:
      ### Increase the Cart Quantity
      index=existing_variation_list.index(product_variation)
      item_id=id[index]
      item=CartItem.objects.get(product=product,id=item_id)
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
  cart=Cart.objects.get(cart_id =_cart_id(request))
  product=Product.objects.get(id=product_id)
  cart_item = CartItem.objects.get(product=product,cart=cart,id=cart_item_id)

  if cart_item.quantity > 1:
    cart_item.quantity -= 1
    cart_item.save()
  else:
    cart_item.delete()

  return redirect('cart')


def remove_cart_item(request,product_id,cart_item_id):
  cart=Cart.objects.get(cart_id =_cart_id(request))
  product=Product.objects.get(id=product_id)
  cart_item = CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
  cart_item.delete()
  return redirect('cart')


def cart(request,total=0,quantity=0,cart_items=None):
  try:
    tax=0
    grand_total=0

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


