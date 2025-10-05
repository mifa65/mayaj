from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .cart_utils import Cart
from .models import *
from .forms import *

# search functionality
def search_view(request):
    query = request.GET.get('q', '')
    sitesettings = SiteSettings.objects.first()
    
    if query:
        # Search in product name, description, and category
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(short_description__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query),
            is_active=True
        ).distinct()
    else:
        products = Product.objects.all()
    
    context = {
        'sitesettings':sitesettings,
        'products': products,
        'query': query,
        'results_count': products.count(),
    }
    return render(request, 'store/search_results.html', context)

# home page logic
def homepageview(request):
    sitesettings = SiteSettings.objects.first()
    herosection = HeroSection.objects.last()
    featured_products = Product.objects.filter(is_active=True,is_featured=True)[:8]
    rotating_image = RotatingShowcaseProduct.objects.filter(is_active=True)[:6]
    combo_offers = ComboOffer.objects.filter(
        is_active=True,
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now(),
        stock_quantity__gt=0
    ).order_by('-is_featured', '-created_at')[:2]

    active_offers = Offer.objects.filter(
        Q(is_active=True) &
        Q(start_date__lte=timezone.now()) &
        Q(end_date__gte=timezone.now())
    ).order_by('-is_featured', '-start_date')[:3]
    combo_offers = combo_offers.prefetch_related(
        'comboproduct_set__product__images'
    )
    context = {
        'sitesettings':sitesettings,
        'herosection':herosection,
        'featured_products': featured_products,
        'rotating_images':rotating_image,
        'combo_offers': combo_offers,
        'active_offers': active_offers,
        
    }
    return render(request, 'store/index.html', context)

# product page logic
def productpageview(request):
    sitesettings = SiteSettings.objects.first()
    products = Product.objects.filter(is_active=True)

    # Pagination
    paginator = Paginator(products, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'sitesettings':sitesettings,
        "page_obj": page_obj,  # paginated products
    }
    return render(request, "store/products.html", context)

# product details page
def productdetailview(request, slug):
    sitesettings = SiteSettings.objects.first()
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Get primary image or first available image
    primary_image = product.images.filter(is_primary=True).first()
    if not primary_image:
        primary_image = product.images.first()
    
    # Get approved reviews count and average rating
    approved_reviews = product.reviews.filter(is_approved=True)
    review_count = approved_reviews.count()
    
    # Calculate average rating
    if review_count > 0:
        total_rating = sum(review.rating for review in approved_reviews)
        average_rating = round(total_rating / review_count, 1)
    else:
        average_rating = 0
    
    # Get featured products
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:4]
    
    # Add is_out_of_stock property to each size
    sizes = list(product.sizes.all())
    for size in sizes:
        size.is_out_of_stock = size.stock_quantity == 0
    
    context = {
        'sitesettings':sitesettings,
        'product': product,
        'primary_image': primary_image,
        'featured_products': featured_products,
        'review_count': review_count,
        'average_rating': average_rating,
        'approved_reviews': approved_reviews,
        'sizes': sizes,  # Pass the modified sizes list
    }
    return render(request, 'store/productdetails.html', context)

# add review to product
def add_review(request, slug):
    if request.method == 'POST':
        product = get_object_or_404(Product, slug=slug)
        # Create a review (you'll need to add validation)
        ProductReview.objects.create(
            product=product,
            customer_name=request.POST.get('customer_name'),
            title=request.POST.get('title', ''),
            comment=request.POST.get('comment'),
            rating=int(request.POST.get('rating', 5)),
            is_approved=False  # Needs admin approval
        )
        messages.success(request, 'Thank you for your review! It will be visible after approval.')
    
    return redirect('product-desc', slug=slug)

# offer page logic 
def offerspageview(request):
    sitesettings = SiteSettings.objects.first()
    combo_offers = ComboOffer.objects.filter(
        is_active=True,
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now(),
        stock_quantity__gt=0
    ).order_by('-is_featured', '-created_at')

    active_offers = Offer.objects.filter(
        Q(is_active=True) &
        Q(start_date__lte=timezone.now()) &
        Q(end_date__gte=timezone.now())
    ).order_by('-is_featured', '-start_date')

    combo_offers = combo_offers.prefetch_related(
        'comboproduct_set__product__images'
    )
    
    context = {
        'sitesettings':sitesettings,
        'combo_offers': combo_offers,
        'active_offers': active_offers,
    }
    return render(request, 'store/offers.html', context)

# about page logic  
def aboutpageview(request):
    sitesettings = SiteSettings.objects.first()
    about_section = AboutSection.objects.filter(is_active=True).first()
    founders = TeamMember.objects.filter(is_active=True, is_founder=True)
    team_members = TeamMember.objects.filter(is_active=True, is_founder=False)
    
    context = {
        'sitesettings':sitesettings,
        'about_section': about_section,
        'founders': founders,
        'team_members': team_members,
    }
    return render(request, 'store/about.html', context)

# contact page logic
def contactpageview(request):
    sitesettings = SiteSettings.objects.first()
    contact_section = ContactPageSettings.objects.filter(is_active=True).first()
    contact_info = ContactInfo.objects.filter(is_active=True)
    social_media = SocialMedia.objects.filter(is_active=True)
    
    # Get subject choices for the form
    subject_choices = ContactMessage.SUBJECT_CHOICES
    
    if request.method == 'POST':
        # Process the form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message_text = request.POST.get('message')
        
        # Create and save the contact message
        contact_message = ContactMessage(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message_text
        )
        contact_message.save()
        
        messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
        return redirect('contact')
    
    context = {
        'sitesettings':sitesettings,
        'contact_section': contact_section,
        'contact_info': contact_info,
        'social_media': social_media,
        'subject_choices': subject_choices,
    }
    return render(request, 'store/contact.html', context)

# return page logic 
def returnpageview(request):
    sitesettings = SiteSettings.objects.first()
    page_settings = ReturnsPageSettings.objects.first()
    policy_points = PolicyPoint.objects.filter(is_active=True).order_by("order")
    steps = ReturnStep.objects.filter(is_active=True).order_by("step_number", "order")
    eligibility_items = EligibilityItem.objects.filter(is_active=True).order_by("type", "order")
    refund_methods = RefundMethod.objects.filter(is_active=True).order_by("order")
    return_reasons = ReturnReason.objects.filter(is_active=True).order_by("order")
    
    # Initialize form with return reasons
    form = ReturnRequestForm(return_reasons=return_reasons)
    
    if request.method == 'POST':
        form = ReturnRequestForm(request.POST, return_reasons=return_reasons)
        if form.is_valid():
            # Create and save ReturnRequest instance
            return_request = ReturnRequest(
                order_number=form.cleaned_data['order_number'],
                customer_email=form.cleaned_data['customer_email'],
                return_type=form.cleaned_data['return_type'],
                reason=form.cleaned_data['reason'],
                additional_details=form.cleaned_data['additional_details'],
                agreed_to_terms=form.cleaned_data['agreed_to_terms']
            )
            return_request.save()
            
            messages.success(request, 'Your return request has been submitted successfully!')
            return redirect('return')  # redirect to return page after succesfull form submit
    
    context = {
        'sitesettings':sitesettings,
        "page_settings": page_settings,
        "policy_points": policy_points,
        "steps": steps,
        "eligibility_items": eligibility_items,
        "refund_methods": refund_methods,
        "return_reasons": return_reasons,
        "form": form,
    }
    return render(request, "store/return.html", context)

# cart pages and cart logic
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        size = request.POST.get('size', None)
        
        cart = Cart(request)
        cart.add(product, quantity, size)
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'cart_count': len(cart),
                'message': 'Product added to cart successfully!'
            })
        
        return redirect('cart_detail')
    
    return redirect('product_list')

def remove_from_cart(request, product_id, size=None):
    cart = Cart(request)
    cart.remove(product_id, size)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'message': 'Product removed from cart!'
        })
    
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    sitesettings = SiteSettings.objects.first()
    
    # Calculate totals
    subtotal = cart.get_total_price()
    discount = 0  # You can implement discount logic later
    shipping = 120 if subtotal > 0 else 0  # Free shipping over certain amount?
    
    context = {
        'sitesettings': sitesettings,
        'cart': cart,
        'subtotal': subtotal,
        'discount': discount,
        'shipping': shipping,
        'total': subtotal - discount + shipping,
    }
    return render(request, 'store/cart.html', context)

def update_cart(request, product_id, size=None):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        
        # For update, we need to find the exact item in cart
        size_key = size or 'no_size'
        item_key = f"{product_id}_{size_key}"
        
        if item_key in cart.cart:
            cart.cart[item_key]['quantity'] = quantity
            cart.save()
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'cart_count': len(cart),
                    'item_total': float(cart.cart[item_key]['price']) * quantity,
                    'cart_total': cart.get_total_price()
                })
    
    return redirect('cart_detail')   

#buy now button logic
def buy_now(request, product_id):
    """Add product to cart and redirect directly to checkout"""
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id, is_active=True)
        quantity = int(request.POST.get('quantity', 1))
        size = request.POST.get('size', None)
        
        # Validate size selection
        if product.sizes.exists() and not size:
            messages.error(request, 'Please select a size.')
            return redirect('product-desc', slug=product.slug)
        
        # Validate stock
        if size:
            product_size = product.sizes.filter(size=size).first()
            if product_size and product.stock_quantity < quantity:
                messages.error(request, f'Only {product.stock_quantity} items available in size {size}.')
                return redirect('product-desc', slug=product.slug)
        elif product.stock_quantity < quantity:
            messages.error(request, f'Only {product.stock_quantity} items available.')
            return redirect('product-desc', slug=product.slug)
        
        # Add to cart
        cart = Cart(request)
        cart.add(product, quantity, size)
        
        # Redirect to checkout
        return redirect('checkout')
    
    return redirect('product-desc', slug=product.slug)

# checkout views logic
def checkout(request):
    cart = Cart(request)
    
    # Redirect if cart is empty
    if not cart:
        messages.warning(request, "Your cart is empty. Add some items before checkout.")
        return redirect('cart_detail')
    
    sitesettings = SiteSettings.objects.first()
    
    # Calculate totals
    subtotal = cart.get_total_price()
    discount = 0
    shipping = 60
    total = subtotal - discount + shipping
    
    # Pre-fill form for authenticated users
    initial_data = {}
    if request.user.is_authenticated:
        # user's full name 
        full_name = f"{request.user.first_name} {request.user.last_name}".strip()
        if not full_name:
            full_name = request.user.username
            
        initial_data = {
            'shipping_full_name': full_name,  # Changed to full_name
            'shipping_email': request.user.email,
        }
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST, initial=initial_data)
        if form.is_valid():
            try:
                # Calculate shipping based on delivery area
                delivery_area = form.cleaned_data.get('delivery_area', 'inside')
                shipping_cost = 60 if delivery_area == 'inside' else 120
                total = subtotal - discount + shipping_cost 
                
                # Create order with single full name field
                order = Order.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    subtotal=subtotal,
                    discount=discount,
                    shipping_cost=shipping_cost,
                    total=total,
                    shipping_full_name=form.cleaned_data['shipping_full_name'],  # Changed to full_name
                    shipping_email=form.cleaned_data['shipping_email'],
                    shipping_phone=form.cleaned_data['shipping_phone'],
                    shipping_address=form.cleaned_data['shipping_address'],
                    shipping_city=form.cleaned_data['shipping_city'],
                    shipping_state=form.cleaned_data.get('shipping_state', ''),
                    shipping_zip_code=form.cleaned_data.get('shipping_zip_code', ''),
                    payment_method=form.cleaned_data.get('payment_method', 'cash_on_delivery'),
                    transaction_id=form.cleaned_data.get('transaction_id', ''),
                    sender_mobile_number=form.cleaned_data.get('sender_mobile_number', ''),
                    notes=form.cleaned_data.get('notes', ''),
                    status='pending',
                    payment_status='pending',
                )
                
                # Create order items
                for item_key, item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        product_name=item['product'].name,
                        size=item.get('size'),
                        quantity=item['quantity'],
                        price=item['price']
                    )
                
                # Clear the cart
                cart.clear()
                
                # Redirect to order success page
                return redirect('order_success', order_id=order.id)
                
            except Exception as e:
                messages.error(request, f"There was an error processing your order: {str(e)}")
                return redirect('checkout')
    else:
        form = CheckoutForm(initial=initial_data)
    
    context = {
        'sitesettings': sitesettings,
        'cart': cart,
        'subtotal': subtotal,
        'discount': discount,
        'shipping': shipping,
        'total': total,
        'form': form,
    }
    return render(request, 'store/checkout.html', context)

def process_order(request):
    if request.method == 'POST':
        cart = Cart(request)
        
        if not cart:
            messages.error(request, "Your cart is empty.")
            return redirect('cart_detail')
        
        try:
            # Create order
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                subtotal=cart.get_total_price(),
                shipping_cost=120,  # Fixed shipping cost for now
                total=cart.get_total_price() + 120,
                shipping_first_name=request.POST.get('first_name'),
                shipping_last_name=request.POST.get('last_name'),
                shipping_email=request.POST.get('email'),
                shipping_phone=request.POST.get('phone'),
                shipping_address=request.POST.get('address'),
                shipping_city=request.POST.get('city'),
                notes=request.POST.get('notes', ''),
                payment_method=request.POST.get('payment_method', 'cash_on_delivery')
            )
            
            # Create order items
            for item_key, item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    product_name=item['product'].name,
                    size=item.get('size'),
                    quantity=item['quantity'],
                    price=item['price']
                )
            
            # Clear the cart
            cart.clear()
            
            # Redirect to order success page WITH order_id parameter
            return redirect('order_success', order_id=order.id)  # Fixed - added order_id
            
        except Exception as e:
            messages.error(request, f"There was an error processing your order: {str(e)}")
            return redirect('checkout')
    
    return redirect('checkout')

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    sitesettings = SiteSettings.objects.first()
    
    context = {
        'sitesettings': sitesettings,
        'order': order,
    }
    return render(request, 'store/order_success.html', context)


def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # Basic security check - ensure user owns the order or is staff
    if request.user != order.user and not request.user.is_staff:
        messages.error(request, "You don't have permission to view this order.")
        return redirect('home')
    
    sitesettings = SiteSettings.objects.first()
    
    context = {
        'sitesettings': sitesettings,
        'order': order,
    }
    return render(request, 'store/order_details.html', context)
    