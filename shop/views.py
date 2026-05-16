from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from .models import Product, Category, Order, OrderItem


def home(request):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')

    if query:
        products = products.filter(name__icontains=query)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'shop/home.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_slug,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    related = Product.objects.filter(category=product.category, available=True).exclude(id=product.id)[:4]
    return render(request, 'shop/product_detail.html', {'product': product, 'related': related})


def cart(request):
    cart_data = request.session.get('cart', {})
    cart_items = []
    total = 0
    for product_id, item in cart_data.items():
        try:
            product = Product.objects.get(id=product_id)
            subtotal = product.price * item['quantity']
            total += subtotal
            cart_items.append({'product': product, 'quantity': item['quantity'], 'subtotal': subtotal})
        except Product.DoesNotExist:
            pass
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total': total})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    pid = str(product_id)
    if pid in cart:
        cart[pid]['quantity'] += 1
    else:
        cart[pid] = {'quantity': 1, 'name': product.name, 'price': str(product.price)}
    request.session['cart'] = cart
    messages.success(request, f'"{product.name}" added to cart!')
    return redirect(request.META.get('HTTP_REFERER', '/'))


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    pid = str(product_id)
    if pid in cart:
        del cart[pid]
        request.session['cart'] = cart
    return redirect('cart')


def update_cart(request, product_id):
    cart = request.session.get('cart', {})
    pid = str(product_id)
    qty = int(request.POST.get('quantity', 1))
    if qty > 0:
        cart[pid] = cart.get(pid, {})
        cart[pid]['quantity'] = qty
    else:
        cart.pop(pid, None)
    request.session['cart'] = cart
    return redirect('cart')


@login_required
def checkout(request):
    cart_data = request.session.get('cart', {})
    if not cart_data:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')

    cart_items = []
    total = 0
    for product_id, item in cart_data.items():
        try:
            product = Product.objects.get(id=product_id)
            subtotal = product.price * item['quantity']
            total += subtotal
            cart_items.append({'product': product, 'quantity': item['quantity'], 'subtotal': subtotal})
        except Product.DoesNotExist:
            pass

    if request.method == 'POST':
        address = request.POST.get('address', '')
        order = Order.objects.create(user=request.user, shipping_address=address, total_price=total)
        for ci in cart_items:
            OrderItem.objects.create(order=order, product=ci['product'], quantity=ci['quantity'], price=ci['product'].price)
        request.session['cart'] = {}
        messages.success(request, f'Order #{order.id} placed successfully!')
        return redirect('order_detail', order_id=order.id)

    return render(request, 'shop/checkout.html', {'cart_items': cart_items, 'total': total})


@login_required
def orders(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'shop/orders.html', {'orders': user_orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/order_detail.html', {'order': order})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect(request.GET.get('next', 'home'))
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
