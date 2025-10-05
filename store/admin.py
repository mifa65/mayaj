from django.contrib import admin
from .models import *


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'announcement_enabled', 'created_at']
    list_editable = ['announcement_enabled']
    
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']
    list_editable = ['is_active']
    
    def has_add_permission(self, request):
        return not HeroSection.objects.exists()

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'order', 'created_at']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'is_primary', 'order']

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1
    fields = ['size', 'stock_quantity']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'discount_price', 'is_active', 'is_featured', 'stock_quantity', 'created_at']
    list_editable = ['price', 'discount_price', 'is_active', 'is_featured', 'stock_quantity']
    list_filter = ['category', 'is_active', 'is_featured', 'is_new', 'gender', 'created_at']
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductSizeInline]
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug','category', 'gender')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'discount_price', 'stock_quantity')
        }),
        ('Content', {
            'fields': ('short_description', 'description')
        }),
        ('Status & Features', {
            'fields': ('is_active', 'is_featured', 'is_new')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'customer_name', 'rating', 'is_approved', 'is_featured', 'created_at']
    list_editable = ['is_approved', 'is_featured']
    list_filter = ['rating', 'is_approved', 'is_featured', 'created_at']
    search_fields = ['customer_name', 'product__name', 'title']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'offer_type', 'discount_percentage', 'is_active', 'is_featured', 'start_date', 'end_date']
    list_editable = ['is_active', 'is_featured']
    list_filter = ['offer_type', 'is_active', 'is_featured', 'start_date', 'end_date']
    search_fields = ['title', 'slug', 'discount_code']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']

class ComboProductInline(admin.TabularInline):
    model = ComboProduct
    extra = 1
    fields = ['product', 'quantity']

@admin.register(ComboOffer)
class ComboOfferAdmin(admin.ModelAdmin):
    list_display = ['name', 'original_price', 'discount_price', 'discount_percentage', 'is_active', 'is_featured', 'start_date', 'end_date']
    list_editable = ['is_active', 'is_featured']
    list_filter = ['is_active', 'is_featured', 'start_date', 'end_date']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ComboProductInline]
    readonly_fields = ['created_at', 'updated_at']

@admin.register(RotatingShowcaseProduct)
class RotatingShowcaseProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['product__name']
    ordering = ['order']

@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']
    list_editable = ['is_active']
    
    def has_add_permission(self, request):
        return not AboutSection.objects.exists()

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'role_type', 'is_active', 'is_founder', 'order', 'created_at']
    list_editable = ['is_active', 'is_founder', 'order']
    list_filter = ['role_type', 'is_active', 'is_founder', 'created_at']
    search_fields = ['name', 'position']
    ordering = ['is_founder', 'order']

@admin.register(ReturnsPageSettings)
class ReturnsPageSettingsAdmin(admin.ModelAdmin):
    list_display = ['header_title', 'is_active', 'created_at']
    list_editable = ['is_active']
    
    def has_add_permission(self, request):
        return not ReturnsPageSettings.objects.exists()

@admin.register(PolicyPoint)
class PolicyPointAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'created_at']
    ordering = ['order']

@admin.register(ReturnStep)
class ReturnStepAdmin(admin.ModelAdmin):
    list_display = ['step_number', 'title', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'created_at']
    ordering = ['step_number', 'order']

@admin.register(EligibilityItem)
class EligibilityItemAdmin(admin.ModelAdmin):
    list_display = ['text', 'type', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['type', 'is_active', 'created_at']
    ordering = ['type', 'order']

@admin.register(RefundMethod)
class RefundMethodAdmin(admin.ModelAdmin):
    list_display = ['payment_method', 'refund_method', 'processing_time', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'created_at']
    ordering = ['order']

@admin.register(ReturnReason)
class ReturnReasonAdmin(admin.ModelAdmin):
    list_display = ['reason', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'created_at']
    ordering = ['order']

@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer_email', 'return_type', 'status', 'created_at']
    list_editable = ['status']
    list_filter = ['return_type', 'status', 'created_at']
    search_fields = ['order_number', 'customer_email', 'reason']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

@admin.register(ContactPageSettings)
class ContactPageSettingsAdmin(admin.ModelAdmin):
    list_display = ['header_title', 'is_active', 'created_at']
    list_editable = ['is_active']
    
    def has_add_permission(self, request):
        return not ContactPageSettings.objects.exists()

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['type', 'title', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['type', 'is_active', 'created_at']
    ordering = ['order']

@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ['platform', 'url', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['platform', 'is_active', 'created_at']
    ordering = ['order']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_resolved', 'created_at']
    list_editable = ['is_resolved']
    list_filter = ['subject', 'is_resolved', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

@admin.register(BusinessHours)
class BusinessHoursAdmin(admin.ModelAdmin):
    list_display = ['day', 'opening_time', 'closing_time', 'is_closed', 'order']
    list_editable = ['opening_time', 'closing_time', 'is_closed', 'order']
    ordering = ['order']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'size', 'quantity', 'price', 'get_total_price']
    
    def has_add_permission(self, request, obj=None):
        return False

    def get_total_price(self, obj):
        return f"৳ {obj.total_price:.2f}"
    get_total_price.short_description = 'Total'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer_name', 'created_at', 'get_order_total']
    list_filter = ['created_at', 'status']
    search_fields = ['order_number', 'shipping_full_name', 'shipping_email']  # Fixed search fields
    readonly_fields = ['created_at', 'updated_at', 'get_order_total']
    inlines = [OrderItemInline]

    # Fixed customer_name method
    def customer_name(self, obj):
        return obj.shipping_full_name  # Use the new single name field
    customer_name.short_description = 'Customer'

    def get_order_total(self, obj):
        total = sum(item.total_price for item in obj.items.all())
        return f"৳ {total:.2f}"
    get_order_total.short_description = 'Total'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_name', 'quantity', 'price', 'get_total_price']
    list_filter = ['order__status']
    readonly_fields = ['order', 'product_name', 'size', 'quantity', 'price']
    
    def get_total_price(self, obj):
        return f"৳ {obj.total_price:.2f}"
    get_total_price.short_description = 'Total'

    def has_add_permission(self, request):
        return False

# Register remaining models that don't need custom admin classes
admin.site.register(ProductImage)
admin.site.register(ProductSize)
admin.site.register(ComboProduct)