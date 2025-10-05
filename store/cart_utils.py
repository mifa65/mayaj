# store/cart_utils.py
from django.conf import settings

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self, product, quantity=1, size=None, update_quantity=False):
        product_id = str(product.id)
        size_key = size or 'no_size'
        item_key = f"{product_id}_{size_key}"
        
        if item_key not in self.cart:
            self.cart[item_key] = {
                'quantity': 0,
                'price': str(product.discount_price or product.price),
                'size': size,
                'product_id': product_id,
            }
        
        if update_quantity:
            self.cart[item_key]['quantity'] = quantity
        else:
            self.cart[item_key]['quantity'] += quantity
        
        self.save()
    
    def remove(self, product_id, size=None):
        size_key = size or 'no_size'
        item_key = f"{product_id}_{size_key}"
        
        if item_key in self.cart:
            del self.cart[item_key]
            self.save()
    
    def save(self):
        self.session.modified = True
    
    def __iter__(self):
        from .models import Product
        product_ids = [item['product_id'] for item in self.cart.values()]
        products = Product.objects.filter(id__in=product_ids)
        
        for product in products:
            for item_key, item in self.cart.items():
                if item['product_id'] == str(product.id):
                    item['product'] = product
                    yield item_key, item
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()