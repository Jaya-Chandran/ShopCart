#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py createadmin
python manage.py shell -c "
from django.contrib.auth.models import User
import os
u = os.environ.get('ADMIN_USER', 'admin')
p = os.environ.get('ADMIN_PASS', 'admin1234')
e = os.environ.get('ADMIN_EMAIL', 'admin@shopcart.com')
if not User.objects.filter(username=u).exists():
    User.objects.create_superuser(u, e, p)
    print(f'Superuser {u} created.')
else:
    print(f'Superuser {u} already exists.')
"
python manage.py shell -c "
from shop.models import Category, Product
if Category.objects.count() == 0:
    cats = [
        ('Electronics', 'electronics'),
        ('Clothing', 'clothing'),
        ('Books', 'books'),
        ('Home & Garden', 'home-garden'),
        ('Sports', 'sports'),
    ]
    for name, slug in cats:
        cat = Category.objects.create(name=name, slug=slug)
        products_data = [
            (f'{name} Item 1', f'{slug}-item-1', 29.99, 50, 'A premium quality product.'),
            (f'{name} Item 2', f'{slug}-item-2', 49.99, 30, 'Best seller in its category.'),
            (f'{name} Item 3', f'{slug}-item-3', 19.99, 100, 'Great value for money.'),
            (f'{name} Item 4', f'{slug}-item-4', 89.99, 15, 'Limited edition item.'),
        ]
        for pname, pslug, price, stock, desc in products_data:
            Product.objects.create(
                category=cat, name=pname, slug=pslug,
                price=price, stock=stock, description=desc
            )
    print('Sample data created.')
else:
    print('Data already exists.')
"
