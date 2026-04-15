# Django Library Management System

A web app to manage books, students, and book issuing — built with Django.

---

## Features

**Admin**
- Manage books, authors, and categories
- Approve/reject book requests
- Track issued/returned books and fines

**Student**
- Register, login, and browse books
- Request books and track due dates

---

## Tech Stack

- Python / Django
- HTML / CSS
- SQLite

---

## Setup

```bash
git clone https://github.com/Mparvathy/django-LibraryManagement.git
cd django-LibraryManagement

python -m venv env
env\Scripts\activate        # Windows
# source env/bin/activate   # Linux/Mac

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`

---

## Project Structure

```
├── librarymanagement/   # Django project settings
├── library/             # Main app
├── templates/           # HTML templates
├── static/              # CSS and static files
├── db.sqlite3
├── manage.py
└── requirements.txt
```

---

## Roadmap

- Email notifications for due dates
- Online fine payment
- REST API
- Mobile responsive UI
- Book reservation system

---

## Author

**Parvathy M** — [GitHub](https://github.com/Mparvathy)

Licensed under the [MIT License](LICENSE).
