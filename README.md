# PennyPilot 💸

PennyPilot is a personal budgeting web app built with Django.  
It helps you track your monthly budget, bills, and recharges with a clean Bootstrap-powered dashboard.

---

## 🚀 Features
- Track remaining monthly budget
- Add and view bills & recharges
- Responsive design with Bootstrap

---

## 🛠 Local development setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/karmakr1920/pennypilot.git
cd pennypilot
````

### 2️⃣ Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set up environment variables

Create a `.env` file at the project root:

```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 5️⃣ Run migrations and start the development server

```bash
python manage.py migrate
python manage.py runserver
```

---

## 📂 Project structure

```
pennypilot/
├── dashboard/        # App for dashboard features
├── pennypilot/       # Project settings and URLs
├── static/           # Static files
├── templates/        # HTML templates
├── db.sqlite3        # Local development database
└── manage.py         # Django management script
