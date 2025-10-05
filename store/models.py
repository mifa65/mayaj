from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.core.validators import EmailValidator
from django.db.models import Q
from django.urls import reverse
from django.conf import settings

# Base model for common fields
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class SiteSettings(TimeStampedModel):
    site_name = models.CharField(max_length=100, default="Mayaj")
    logo = models.ImageField(upload_to='site/logo/', blank=True, null=True)
    favicon = models.ImageField(upload_to='site/favicon/', blank=True, null=True)
    footer_description = RichTextField(blank=True,null=True,default="Step into style with our premium collection of footwear for every occasion.")
    footer_copyright_text = models.TextField(blank=True,null=True,default="Mayaj. All rights reserved.")
    announcement_text = models.CharField(max_length=200, default="Free shipping on all orders over ৳50! 🚚")
    announcement_enabled = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return "Site Configuration"

class HeroSection(TimeStampedModel):
    title = models.CharField(max_length=200, default="Step Into Style With Mayaj!")
    subtitle = models.TextField(default="Discover the perfect blend of comfort and fashion with our exclusive shoe collection")
    primary_button_text = models.CharField(max_length=50, default="Shop Now")
    primary_button_link = models.CharField(max_length=200, default="#products")
    secondary_button_text = models.CharField(max_length=50, default="Limited Offers")
    secondary_button_link = models.CharField(max_length=200, default="#offers")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Hero Section"
    
    def __str__(self):
        return "Hero Section"
    
    def save(self, *args, **kwargs):
        if not self.pk and HeroSection.objects.exists():
            existing = HeroSection.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)

class Category(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class Product(TimeStampedModel):
    GENDER_CHOICES = [
        ('M', 'Men'),
        ('F', 'Women'),
        ('U', 'Unisex'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = RichTextField()
    short_description = models.TextField(max_length=500, blank=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})
    
    def is_in_stock(self):
        return self.stock_quantity > 0
    
    @property
    def get_discount_percentage(self):
        if self.discount_price and self.price > 0:
            discount_amount = self.price - self.discount_price
            return int((discount_amount / self.price) * 100)
        return 0

    def get_average_rating(self):
        approved_reviews = self.reviews.filter(is_approved=True)
        if approved_reviews.exists():
            total_rating = sum(review.rating for review in approved_reviews)
            return round(total_rating / approved_reviews.count(), 1)
        return 0

class ProductImage(TimeStampedModel):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-is_primary', 'created_at']
    
    def __str__(self):
        return f"Image for {self.product.name}"

class ProductSize(models.Model):
    product = models.ForeignKey(Product, related_name='sizes', on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    stock_quantity = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ['product', 'size']
        ordering = ['size']
    
    def __str__(self):
        return f"{self.product.name} - {self.size}"

class ProductReview(TimeStampedModel):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200)
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review for {self.product.name} by {self.customer_name}"


class Offer(TimeStampedModel):
    OFFER_TYPES = [
        ('summer_sale', 'Summer Sale'),
        ('welcome_offer', 'Welcome Offer'),
        ('free_shipping', 'Free Shipping'),
        ('discount_code', 'Discount Code'),
        ('clearance', 'Clearance Sale'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    short_description = models.TextField(max_length=500, blank=True)
    offer_type = models.CharField(max_length=50, choices=OFFER_TYPES)
    discount_percentage = models.PositiveIntegerField(
        default=0, 
        validators=[MaxValueValidator(100)], 
        blank=True, 
        null=True
    )
    discount_code = models.CharField(max_length=50, blank=True)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return self.title
    
    @property
    def gradient_classes(self):
        gradients = {
            'summer_sale': 'from-purple-600 via-indigo-600 to-blue-600',
            'welcome_offer': 'from-amber-600 via-orange-600 to-red-600',
            'free_shipping': 'from-emerald-600 via-teal-600 to-cyan-600',
            'discount_code': 'from-pink-600 via-rose-600 to-red-600',
            'clearance': 'from-gray-600 via-gray-700 to-gray-800',
        }
        return gradients.get(self.offer_type, 'from-purple-600 via-indigo-600 to-blue-600')
    
    @property
    def badge_text(self):
        days_remaining = (self.end_date - timezone.now()).days
        if days_remaining <= 3:
            return "Ending Soon"
        elif self.offer_type == 'welcome_offer':
            return "New Customers"
        elif self.offer_type == 'free_shipping':
            return "Ongoing"
        else:
            return "Special Offer"
    
    @property
    def icon_class(self):
        icons = {
            'summer_sale': 'fas fa-percent',
            'welcome_offer': 'fas fa-gift',
            'free_shipping': 'fas fa-truck',
            'discount_code': 'fas fa-tag',
            'clearance': 'fas fa-fire',
        }
        return icons.get(self.offer_type, 'fas fa-percent')
    
    def is_currently_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date and self.is_active

class ComboOffer(TimeStampedModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = RichTextField()
    products = models.ManyToManyField(Product, through='ComboProduct')
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    stock_quantity = models.PositiveIntegerField(default=0)
    badge_text = models.CharField(max_length=50, default="POPULAR")
    savings_badge_text = models.CharField(max_length=50, default="SAVE 25%")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def savings_amount(self):
        return self.original_price - self.discount_price
    
    @property
    def is_active_now(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date and self.is_active and self.stock_quantity > 0
    
class ComboProduct(models.Model):
    combo_offer = models.ForeignKey(ComboOffer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ['combo_offer', 'product']
    
    def __str__(self):
        return f"{self.product.name} in {self.combo_offer.name}"

class RotatingShowcaseProduct(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        unique_together = ['product', 'order']
    
    def __str__(self):
        return f"{self.product.name} (Position: {self.order})"

class AboutSection(TimeStampedModel):
    title = models.CharField(max_length=200, default="Who We Are")
    content = RichTextField(default="Mayaj একটি আধুনিক ই-কমার্স ব্র্যান্ড যা উচ্চমানের পণ্য গ্রাহকদের কাছে পৌঁছে দেয়। আমাদের লক্ষ্য হল গ্রাহকদের জন্য সহজ, সাশ্রয়ী এবং নির্ভরযোগ্য অনলাইন শপিং অভিজ্ঞতা তৈরি করা।")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "About Section"
    
    def __str__(self):
        return "About Section"
    
    def save(self, *args, **kwargs):
        if not self.pk and AboutSection.objects.exists():
            existing = AboutSection.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)

class TeamMember(TimeStampedModel):
    ROLE_CHOICES = [
        ('founder', 'Founder'),
        ('management', 'Management'),
        ('technical', 'Technical'),
        ('marketing', 'Marketing'),
        ('finance', 'Finance'),
        ('operations', 'Operations'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    role_type = models.CharField(max_length=20, choices=ROLE_CHOICES, default='other')
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='team/')
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_founder = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['is_founder', 'order', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.position}"

class ReturnsPageSettings(TimeStampedModel):
    # Header Section
    header_title = models.CharField(max_length=200, default="Returns & Exchanges")
    header_subtitle = models.CharField(max_length=300, default="We want you to be completely satisfied with your Mayaj purchase")
    
    # Policy Section
    policy_title = models.CharField(max_length=200, default="Our Return Policy")
    
    # Process Section
    process_title = models.CharField(max_length=200, default="How to Return or Exchange")
    
    # Detailed Policy Section
    detailed_policy_title = models.CharField(max_length=200, default="Detailed Return Policy")
    
    # Form Section
    form_title = models.CharField(max_length=200, default="Initiate Return Request")
    
    # Contact Section
    contact_title = models.CharField(max_length=200, default="Need Help With Your Return?")
    contact_subtitle = models.CharField(max_length=300, default="Our customer support team is here to assist you")
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Returns Page Settings"
    
    def __str__(self):
        return "Returns Page Settings"
    
    def save(self, *args, **kwargs):
        if not self.pk and ReturnsPageSettings.objects.exists():
            existing = ReturnsPageSettings.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)

class PolicyPoint(TimeStampedModel):
    ICON_CHOICES = [
        ('calendar-check', 'Calendar Check'),
        ('box-open', 'Box Open'),
        ('truck', 'Truck'),
        ('phone', 'Phone'),
        ('box', 'Box'),
        ('truck-loading', 'Truck Loading'),
        ('check-circle', 'Check Circle'),
        ('exchange-alt', 'Exchange'),
        ('money-bill-wave', 'Money Bill'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, choices=ICON_CHOICES)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title

class ReturnStep(TimeStampedModel):
    step_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, choices=PolicyPoint.ICON_CHOICES)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['step_number', 'order']
    
    def __str__(self):
        return f"Step {self.step_number}: {self.title}"

class EligibilityItem(TimeStampedModel):
    ELIGIBILITY_TYPE_CHOICES = [
        ('eligible', 'Eligible'),
        ('not_eligible', 'Not Eligible'),
    ]
    
    text = models.CharField(max_length=300)
    type = models.CharField(max_length=20, choices=ELIGIBILITY_TYPE_CHOICES)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['type', 'order']
    
    def __str__(self):
        return self.text

class RefundMethod(TimeStampedModel):
    payment_method = models.CharField(max_length=100)
    refund_method = models.CharField(max_length=100)
    processing_time = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.payment_method} → {self.refund_method}"

class ReturnReason(TimeStampedModel):
    reason = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.reason

class ReturnRequest(TimeStampedModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    
    RETURN_TYPE_CHOICES = [
        ('refund', 'Return for Refund'),
        ('size_exchange', 'Exchange for Size'),
        ('color_exchange', 'Exchange for Color'),
    ]
    
    order_number = models.CharField(max_length=100)
    customer_email = models.EmailField()
    return_type = models.CharField(max_length=20, choices=RETURN_TYPE_CHOICES)
    reason = models.CharField(max_length=200)  # Simple char field instead of FK
    additional_details = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    agreed_to_terms = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Return #{self.id} - {self.order_number}"
    
class ContactPageSettings(TimeStampedModel):
    # Header Section
    header_title = models.CharField(max_length=200, default="Get in Touch")
    header_subtitle = models.CharField(max_length=300, default="We'd love to hear from you. Our friendly team is always here to chat.")
    
    # Contact Info Section
    contact_info_title = models.CharField(max_length=200, default="Contact Information")
    
    # Form Section
    form_title = models.CharField(max_length=200, default="Send us a Message")
    
    # Map Section
    map_title = models.CharField(max_length=200, default="Our Location")
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Contact Page Settings"
    
    def __str__(self):
        return "Contact Page Settings"
    
    def save(self, *args, **kwargs):
        if not self.pk and ContactPageSettings.objects.exists():
            existing = ContactPageSettings.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)

class ContactInfo(TimeStampedModel):
    CONTACT_TYPE_CHOICES = [
        ('location', 'Location'),
        ('phone', 'Phone'),
        ('email', 'Email'),
        ('hours', 'Working Hours'),
    ]
    
    type = models.CharField(max_length=20, choices=CONTACT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    content = models.TextField()
    icon = models.CharField(max_length=50, default="fas fa-circle")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.get_type_display()}: {self.title}"

class SocialMedia(TimeStampedModel):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
        ('youtube', 'YouTube'),
        ('linkedin', 'LinkedIn'),
        ('pinterest', 'Pinterest'),
    ]
    
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()
    icon_class = models.CharField(max_length=50, default="fab fa-circle")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.get_platform_display()

class ContactMessage(TimeStampedModel):
    SUBJECT_CHOICES = [
        ('general', 'General Inquiry'),
        ('product', 'Product Question'),
        ('order', 'Order Issue'),
        ('return', 'Return Request'),
        ('complaint', 'Complaint'),
        ('compliment', 'Compliment'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator()])
    phone = models.CharField(max_length=15, blank=True)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES, default='general')
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

class BusinessHours(TimeStampedModel):
    DAY_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]
    
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    is_closed = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = "Business Hours"
    
    def __str__(self):
        if self.is_closed:
            return f"{self.get_day_display()}: Closed"
        return f"{self.get_day_display()}: {self.opening_time.strftime('%I:%M %p')} - {self.closing_time.strftime('%I:%M %p')}"
    
class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cash_on_delivery', 'Cash on Delivery'),
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
        ('rocket', 'Rocket'),
    ]

    # Order Information
    order_number = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                            null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash_on_delivery')
    
    # Pricing
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    # Shipping Information - CHANGED TO SINGLE FULL NAME FIELD
    shipping_full_name = models.CharField(max_length=200)  # Combined first + last name
    shipping_email = models.EmailField()
    shipping_phone = models.CharField(max_length=15)
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100, blank=True, null=True)
    shipping_zip_code = models.CharField(max_length=10, blank=True, null=True)
    
    # Payment Information (for mobile payments)
    transaction_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Transaction ID")
    sender_mobile_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Sender's Mobile Number")
    
    # Additional
    notes = models.TextField(blank=True, null=True)
    admin_notes = models.TextField(blank=True, null=True, help_text="Internal notes for order processing")
    
    # Tracking Information
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    shipping_carrier = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.order_number}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        
        # Update paid_at timestamp when payment status changes to paid
        if self.pk:
            original = Order.objects.get(pk=self.pk)
            if original.payment_status != 'paid' and self.payment_status == 'paid':
                self.paid_at = timezone.now()
        elif self.payment_status == 'paid' and not self.paid_at:
            self.paid_at = timezone.now()
            
        super().save(*args, **kwargs)
    
    def generate_order_number(self):
        """Generate a unique order number"""
        from datetime import datetime
        import random
        timestamp = datetime.now().strftime('%Y%m%d%H%M')
        random_str = str(random.randint(100, 999))
        return f"ORD{timestamp}{random_str}"
    
    @property
    def customer_name(self):
        """Get customer full name"""
        return self.shipping_full_name  # Simplified - just return the full name
    
    @property
    def is_paid(self):
        """Check if order is paid"""
        return self.payment_status == 'paid'
    
    @property
    def can_be_cancelled(self):
        """Check if order can be cancelled"""
        return self.status in ['pending', 'confirmed']
    
    def mark_as_paid(self, transaction_id=None, sender_number=None):
        """Mark order as paid with transaction details"""
        self.payment_status = 'paid'
        self.paid_at = timezone.now()
        
        if transaction_id:
            self.transaction_id = transaction_id
        if sender_number:
            self.sender_mobile_number = sender_number
            
        self.save()
    
    def get_payment_method_display_name(self):
        """Get formatted payment method name"""
        method_map = {
            'cash_on_delivery': 'Cash on Delivery',
            'bkash': 'bKash',
            'nagad': 'Nagad',
            'rocket': 'Rocket'
        }
        return method_map.get(self.payment_method, self.payment_method)
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    product_name = models.CharField(max_length=200)
    size = models.CharField(max_length=10, blank=True, null=True)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Store product details at time of purchase
    product_image = models.ImageField(upload_to='order_items/', blank=True, null=True)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return f"{self.quantity} x {self.product_name}"
    
    @property
    def total_price(self):
        """Calculate total price for this line item"""
        if self.price is None or self.quantity is None:
            return 0
        return self.price * self.quantity
    
    def save(self, *args, **kwargs):
        # Store product details at time of purchase
        if self.product and not self.product_name:
            self.product_name = self.product.name
        
        
        if self.product and not self.product_image and self.product.images.first():
            self.product_image = self.product.images.first().image
            
        super().save(*args, **kwargs)    
        