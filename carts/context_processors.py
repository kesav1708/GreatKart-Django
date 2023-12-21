from .models import Cart,CartItem
from .views import _cart_id

def counter(request):
  cart_count=0
  if 'admin' in request.path:
    return {}
  
  else:
    try:
      cart=Cart.objects.filter(cart_id=_cart_id(request))

      if request.user.is_authenticated:
        ## If user logged in , Getting the Cartitems for the user.
        cart_items=CartItem.objects.all().filter(user=request.user)

      else:
        ## Getting Only One cart id .
        cart_items=CartItem.objects.all().filter(cart=cart[:1])

      for cart_item in cart_items:
        cart_count += cart_item.quantity

    except Cart.DoesNotExist:
      cart_count = 0

  return {'cart_count' : cart_count}

