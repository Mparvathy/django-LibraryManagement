📚 Django Library Management System

A Library Management System built using the Django framework that helps manage books, students, and book issuing processes in a digital way.

This web application allows administrators to manage library resources efficiently and enables students to browse and request books online.

🚀 Features
👩‍🎓 Student / User

User registration and login

Browse all available books

Search books by title, author, or category

Request books from the library

View issued books

Track due dates for returning books

Check fines for overdue books

🛠 Admin

Admin login and dashboard

Add, update, and delete books

Manage authors and categories

View all book issue requests

Approve or reject book requests

Manage student accounts

Track issued and returned books

Calculate and manage fines

🧰 Technologies Used
Technology	Description
Python	Programming language
Django	Web framework
HTML	Frontend structure
CSS	Styling
SQLite	Default database

Django enables CRUD operations (Create, Read, Update, Delete) which are essential for managing library records such as books, users, and issues.

📂 Project Structure
django-LibraryManagement
│
├── librarymanagement/     # Main Django project
├── library/               # Library application
├── templates/             # HTML templates
├── static/                # CSS and static files
├── db.sqlite3             # SQLite database
├── manage.py              # Django management file
└── requirements.txt       # Python dependencies

⚙️ Installation Guide
1️⃣ Clone the Repository
git clone https://github.com/Mparvathy/django-LibraryManagement.git

2️⃣ Move to the Project Folder
cd django-LibraryManagement

3️⃣ Create Virtual Environment
python -m venv env

4️⃣ Activate Virtual Environment

Windows

env\Scripts\activate


Linux / Mac

source env/bin/activate

5️⃣ Install Dependencies
pip install -r requirements.txt

6️⃣ Run Database Migrations
python manage.py migrate

7️⃣ Start the Server
python manage.py runserver

🌐 Usage

Open your browser and visit:

http://127.0.0.1:8000/


You can now:

Register as a student

Login to the system

Browse available books

Request and manage book issues

📸 Screenshots

You can add screenshots such as:

Login Page

Registration Page

Home Page

Book List

Admin Dashboard

Example:

/screenshots/login.png
/screenshots/dashboard.png

📌 Future Improvements

Email notifications for due dates

Online fine payment

REST API support

Mobile responsive UI

Book reservation system

👩‍💻 Author

Parvathy M

GitHub:
https://github.com/Mparvathy

📜 License

This project is licensed under the MIT License.
