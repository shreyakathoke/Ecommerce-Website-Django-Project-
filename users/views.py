from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import ProfileForm
from .models import Profile
from django.contrib.auth import authenticate, login
from django.contrib.admin.views.decorators import staff_member_required


from .forms import RegisterForm, ProductSearchForm, ProductForm
from .models import Product, Category, Cart, CartItem, Wishlist, Order, OrderItem

# --------------------- GENERAL VIEWS --------------------- #
def base_view(request):
    return render(request, "users/base.html")


@login_required(login_url='users:login')
def shop_view(request):
    # Get all products
    all_products = Product.objects.all()
    
    # Get all categories
    categories = Category.objects.all()
    
    # Prepare a dictionary mapping each category to its products
    category_products = {}
    for category in categories:
        category_products[category.name] = Product.objects.filter(category=category)
    
    # Featured products and best sellers
    featured_products = Product.objects.filter(is_featured=True)
    best_sellers = Product.objects.order_by('-sold')[:10]

    return render(request, "users/shop.html", {
        "all_products": all_products,
        "category_products": category_products,
        "featured_products": featured_products,
        "best_sellers": best_sellers
    })




def contact_view(request):
    return render(request, "users/contact.html")


def about_view(request):
    return render(request, "users/about.html")


from django.contrib.auth.decorators import login_required





# --------------------- AUTH VIEWS --------------------- #
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            messages.success(request, f"Account created for {user.username}!")
            return redirect('users:shop')
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})




def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)  # Create the form

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            # Ensure profile exists
            Profile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('users:shop')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'users/login.html', {'form': form})  # Pass form to template


@login_required(login_url='users:login')
def logout_view(request):
    logout(request)
    messages.info(request, "You have logged out successfully.")
    return redirect("users:base")


@login_required(login_url='users:login')
def profile_view(request):
    return render(request, "users/profile.html", {"user": request.user})


# --------------------- CART --------------------- #
def view_cart(request):
    # Get cart for logged-in user
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(cart__user=request.user)
        cart_total = sum([item.total for item in cart_items])
        shipping_cost = 10  # Example flat shipping
    else:
        cart_items = []
        cart_total = 0
        shipping_cost = 0

    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'shipping_cost': shipping_cost,
        'cart_count': cart_items.count(),
        'wishlist_count': 0,  # replace with real wishlist count if needed
    }
    return render(request, 'users/cart.html', context)



@login_required(login_url='users:login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user,)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    messages.success(request, f"{product.name} added to cart.")
    return redirect("users:view_cart")  # redirect to cart page


@login_required(login_url='users:login')
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.info(request, "Item removed from cart.")
    return redirect("users:view_cart")

from users.models import Product


from .models import Product, Wishlist

# users/views.py
from django.shortcuts import render

@login_required
def add_to_wishlist(request, product_id):
    # Get the product or 404
    product = get_object_or_404(Product, id=product_id)

    # Get or create a wishlist for this user
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    # Add the product if it's not already in the wishlist
    if not wishlist.items.filter(id=product.id).exists():
        wishlist.items.add(product)

    # Redirect to wishlist page
    return redirect('users:wishlist')


@login_required
def wishlist_view(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist_items = wishlist.items.all()
    context = {
        'wishlist_items': wishlist_items,
        'wishlist_count': wishlist_items.count(),
    }
    return render(request, 'users/wishlist.html', context)


@login_required(login_url='users:login')
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    wishlist.items.remove(product)
    messages.success(request, f"{product.name} removed from wishlist.")
    return redirect("users:wishlist")


# --------------------- CHECKOUT --------------------- #
from .forms import CheckoutForm  # <-- we’ll use a Django form for shipping details

@login_required(login_url='users:login')
def checkout(request, product_id=None):
    shipping_cost = 50  # example shipping cost

    if product_id:  # Single product checkout
        product = get_object_or_404(Product, id=product_id)
        items = None
        subtotal = product.price
        total = subtotal + shipping_cost
    else:  # Cart checkout
        cart = get_object_or_404(Cart, user=request.user)
        items = cart.items.all()

        if not items.exists():
            messages.error(request, "Your cart is empty!")
            return redirect("users:shop")

        subtotal = sum(item.product.price * item.quantity for item in items)
        total = subtotal + shipping_cost
        product = None

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                seller=(product.seller if product else items[0].product.seller),
                
                status="Pending"
            )

            if product:  # Single product order
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=1,
                    size=request.POST.get("size", None),
                    price=product.price
                )
            else:  # Multiple cart items
                for item in items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        size=item.size if hasattr(item, 'size') else None,
                        price=item.product.price
                    )
                # Remove items from cart after order
                items.delete()

            messages.success(request, "Your order has been placed successfully! 🎉")
            return redirect("users:order_success")
    else:
        form = CheckoutForm()

    return render(request, "users/checkout.html", {
        "form": form,
        "items": items,
        "product": product,
        "subtotal": subtotal,
        "shipping_cost": shipping_cost,
        "total": total
    })



# --------------------- PRODUCTS --------------------- #
def product_list(request):
    products = Product.objects.all()
    form = ProductSearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data.get("query")
        if query:
            products = products.filter(name__icontains=query)
    return render(request, "users/product_list.html", {"products": products, "form": form})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "users/product_details.html", {"product": product})


def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()
    return render(request, "users/category.html", {"category": category, "products": products})


# --------------------- SELLER DASHBOARD --------------------- #



@staff_member_required(login_url='users:login')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user   # still assign seller
            product.save()
            messages.success(request, "Product added successfully!")
            return redirect('users:seller_dashboard')
    else:
        form = ProductForm()
    return render(request, 'users/add_product.html', {'form': form})




@login_required(login_url='users:login')
def seller_dashboard(request):
    # Only fetch products created by this seller (logged-in user)
    products = Product.objects.filter(seller=request.user)

    # Example stats (you can adjust later)
    total_orders = 0
    total_revenue = 0

    return render(request, "users/seller_dashboard.html", {
        "products": products,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
    })



@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect("users:seller_dashboard")
    else:
        form = ProductForm(instance=product)
    
    return render(request, "users/edit_product.html", {"form": form, "product": product})


@login_required(login_url='users:login')
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully!")
        return redirect("users:seller_dashboard")

    return render(request, "users/delete_product.html", {"product": product})





from django.shortcuts import get_object_or_404

@login_required
def edit_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile')  # redirect to profile page
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'users/edit_profile.html', {'form': form})


from django.shortcuts import render

def order_success(request):
    return render(request, 'users/order_success.html')



def search(request):
    query = request.GET.get("q", "")
    results = Product.objects.filter(name__icontains=query) if query else []
    return render(request, "users/search_results.html", {"query": query, "results": results})

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import CartItem

@require_POST
def update_cart_ajax(request):
    item_id = request.POST.get('item_id')
    quantity = request.POST.get('quantity')

    try:
        item = CartItem.objects.get(id=item_id)
        item.quantity = quantity
        item.save()
        # Return updated totals
        return JsonResponse({
            'item_total': item.get_total_price(),
            'cart_total': item.cart.get_total_price(),
            'shipping': item.cart.get_shipping_cost()
        })
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
    

def update_cart_ajax(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 1))
        item = CartItem.objects.get(id=item_id)
        item.quantity = quantity
        item.save()

        cart = item.cart
        item_total = item.total
        cart_total = cart.total
        shipping = cart.shipping_cost  # or set a fixed value

        return JsonResponse({'item_total': item_total, 'cart_total': cart_total, 'shipping': shipping})

def remove_cart_ajax(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = CartItem.objects.get(id=item_id)
        cart = item.cart
        item.delete()

        cart_total = cart.total
        shipping = cart.shipping_cost  # or fixed value
        return JsonResponse({'cart_total': cart_total, 'shipping': shipping})
    

@login_required(login_url='users:login')
def order_summary(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    # Calculate total price per item and overall subtotal
    for item in items:
        item.total_price = item.product.price * item.quantity  # Add total_price to each item

    subtotal = sum(item.total_price for item in items)
    shipping_fee = 50  # example fixed shipping
    total_price = subtotal + shipping_fee

    context = {
        "order": {
            "items": items,
            "subtotal": subtotal,
            "shipping_fee": shipping_fee,
            "total_price": total_price
        }
    }
    return render(request, "users/order_summary.html", )




@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "users/my_orders.html", {"orders": orders})



@login_required
def remove_cart_ajax(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        item.delete()

        # recalculate totals
        cart_items = CartItem.objects.filter(cart__user=request.user)
        cart_total = sum(i.product.price * i.quantity for i in cart_items)
        shipping = 50 if cart_total < 500 else 0

        return JsonResponse({
            "cart_total": cart_total,
            "shipping": shipping
        })
