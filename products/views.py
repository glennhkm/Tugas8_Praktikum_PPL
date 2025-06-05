from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from .models import Product, Review
from .forms import ProductForm, ReviewForm

def is_admin(user):
    """Check if user is an admin."""
    return user.is_superuser

def product_list(request):
    """Display a list of all products."""
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    sort = request.GET.get('sort', '-updated_at')
    
    # Base queryset
    products = Product.objects.all()
    
    # Apply filters
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(brand__icontains=query)
        )
    
    if category:
        products = products.filter(category=category)
    
    # Apply sorting
    products = products.order_by(sort)
    
    # Get categories from model choices instead of database
    categories_display = Product._meta.get_field('category').choices
    
    # Pagination
    paginator = Paginator(products, 9)  # 9 products per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories_display': categories_display,
        'query': query,
        'selected_category': category,
        'sort': sort
    }
    
    return render(request, 'products/product_list.html', context)

def product_detail(request, pk):
    """Display details of a specific product."""
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.all()
    
    # Check if user has already reviewed this product
    user_review = None
    can_review = False
    
    if request.user.is_authenticated:
        user_review = Review.objects.filter(product=product, user=request.user).first()
        can_review = user_review is None
    
    # Handle new review submission
    if request.method == 'POST' and can_review:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted!')
            return redirect('product_detail', pk=pk)
    else:
        form = ReviewForm()
    
    # Related products (same category)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'reviews': reviews,
        'review_form': form,
        'user_review': user_review,
        'can_review': can_review,
        'related_products': related_products,
    }
    
    return render(request, 'products/product_detail.html', context)

@login_required
def edit_review(request, product_pk, review_pk):
    """Edit an existing review."""
    review = get_object_or_404(Review, pk=review_pk, user=request.user)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your review has been updated!')
            return redirect('product_detail', pk=product_pk)
    else:
        form = ReviewForm(instance=review)
    
    context = {
        'form': form,
        'product': review.product,
    }
    
    return render(request, 'products/edit_review.html', context)

@login_required
def delete_review(request, product_pk, review_pk):
    """Delete an existing review."""
    review = get_object_or_404(Review, pk=review_pk, user=request.user)
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Your review has been deleted!')
        return redirect('product_detail', pk=product_pk)
    
    context = {
        'review': review,
        'product': review.product,
    }
    
    return render(request, 'products/delete_review.html', context)

# Admin-only views
@user_passes_test(is_admin)
def product_create(request):
    """Admin-only: Create a new product."""
    messages.info(request, 'Product management is available in the admin panel only.')
    return redirect('admin:products_product_add')

@user_passes_test(is_admin)
def product_update(request, pk):
    """Admin-only: Update an existing product."""
    messages.info(request, 'Product management is available in the admin panel only.')
    return redirect('admin:products_product_change', pk)

@user_passes_test(is_admin)
def product_delete(request, pk):
    """Admin-only: Delete an existing product."""
    messages.info(request, 'Product management is available in the admin panel only.')
    return redirect('admin:products_product_delete', pk)
