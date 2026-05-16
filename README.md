# 🛒 ShopCart — Django E-Commerce

A full-featured Django shopping cart application with user authentication, product catalog, cart management, and order tracking.

## Features

- 🏪 Product catalog with categories & search
- 🛒 Session-based shopping cart
- 👤 User registration & authentication
- 📦 Order placement & tracking
- 🔧 Django Admin panel
- 📱 Responsive design

## Tech Stack

- **Backend**: Django 4.2
- **Database**: PostgreSQL (Render) / SQLite (local)
- **Static Files**: WhiteNoise
- **Server**: Gunicorn
- **Deployment**: Render

---

## 🚀 Deploy to Render (Step-by-Step)

### Option 1: Using render.yaml (Recommended)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/ShopCart.git
   git push -u origin main
   ```

2. **Connect to Render**
   - Go to [render.com](https://render.com) and sign up/login
   - Click **"New +"** → **"Blueprint"**
   - Connect your GitHub account
   - Select your **ShopCart** repository
   - Render will auto-detect `render.yaml` and create:
     - A **Web Service** (Django app)
     - A **PostgreSQL database**
   - Click **"Apply"**

3. **Done!** Your app will be live at `https://shopcart.onrender.com`

---

### Option 2: Manual Setup on Render

1. **Create PostgreSQL Database**
   - Render Dashboard → New → PostgreSQL
   - Name: `shopcart-db`, Plan: Free
   - Copy the **Internal Database URL**

2. **Create Web Service**
   - New → Web Service → Connect GitHub repo
   - Configure:
     | Setting | Value |
     |---------|-------|
     | **Name** | `shopcart` |
     | **Environment** | `Python 3` |
     | **Build Command** | `bash build.sh` |
     | **Start Command** | `gunicorn shopcart.wsgi:application --bind 0.0.0.0:$PORT` |

3. **Set Environment Variables**
   | Key | Value |
   |-----|-------|
   | `SECRET_KEY` | (auto-generate a strong key) |
   | `DEBUG` | `False` |
   | `DATABASE_URL` | (paste your PostgreSQL URL) |
   | `ADMIN_USER` | `admin` |
   | `ADMIN_PASS` | `yourpassword` |
   | `ADMIN_EMAIL` | `admin@example.com` |

4. Click **"Create Web Service"**

---

## 💻 Local Development

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/ShopCart.git
cd ShopCart

# Install dependencies
pip install -r requirements.txt

# Set env
export DEBUG=True
export SECRET_KEY=local-dev-secret-key

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data (optional)
bash build.sh

# Start server
python manage.py runserver
```

Visit: http://127.0.0.1:8000  
Admin: http://127.0.0.1:8000/admin

---

## 📁 Project Structure

```
ShopCart/
├── shopcart/           # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── shop/               # Main app
│   ├── models.py       # Product, Category, Order
│   ├── views.py        # All views
│   ├── urls.py
│   ├── admin.py
│   ├── context_processors.py
│   └── templates/shop/
│       ├── base.html
│       ├── home.html
│       ├── product_detail.html
│       ├── cart.html
│       ├── checkout.html
│       ├── orders.html
│       ├── order_detail.html
│       ├── login.html
│       └── register.html
├── requirements.txt
├── render.yaml         # Render Blueprint config
├── build.sh            # Render build script
├── manage.py
└── README.md
```

## Admin Panel

Access at `/admin/` with your superuser credentials to:
- Add/edit products and categories
- Manage orders and update status
- View user accounts
