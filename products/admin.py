from django.contrib import admin
from django import forms
from .models import Product, Review
from .supabase_storage import upload_image_to_supabase, delete_image_from_supabase
from django.utils.safestring import mark_safe

class ProductAdminForm(forms.ModelForm):
    product_image = forms.ImageField(required=False)
    
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['image_url', 'image_path']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('name', 'price', 'stock', 'brand', 'category', 'featured', 'average_rating', 'review_count', 'updated_at')
    list_filter = ('category', 'brand', 'featured')
    search_fields = ('name', 'description')
    ordering = ('-updated_at',)
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image_url:
            return mark_safe(f'<img src="{obj.image_url}" width="150" height="150" style="object-fit: cover;" />')
        return "No image"
    
    image_preview.short_description = 'Image Preview'
    
    def save_model(self, request, obj, form, change):
        if 'product_image' in form.files:
            # Delete old image if it exists
            if obj.image_path:
                delete_image_from_supabase(obj.image_path)
            
            # Upload new image
            image_file = form.files['product_image']
            file_path, file_url = upload_image_to_supabase(image_file)
            
            if file_path and file_url:
                obj.image_path = file_path
                obj.image_url = file_url
        
        super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
        # Delete image from Supabase when product is deleted
        if obj.image_path:
            delete_image_from_supabase(obj.image_path)
        super().delete_model(request, obj)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')
    raw_id_fields = ('product', 'user')
