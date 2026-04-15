from django.shortcuts import render,redirect,get_object_or_404
from django. contrib.auth  import authenticate,login,logout
from .models import customuser,Book,BookRequest,CartItem,Cart,Order,Branch,Branch
from .models import OrderItem
from .forms import BookForm,StudentSignupForm,BookRequestForm,DueDateForm,DiectBookIssueForm,FinePaymentForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test,login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import BookIssue, Book
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from xhtml2pdf import pisa
from io import BytesIO
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import customuser

def render_to_pdf(template_src, context_dict={}):
    from django.template.loader import get_template
    from io import BytesIO
    from xhtml2pdf import pisa
    from django.http import HttpResponse 
    template = get_template(template_src)
    html = template.render(context_dict)  # Pass context_dict directly
    result = BytesIO()
    pdf = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse("Error generating PDF", content_type='text/plain')

def is_user(user):
    return user.is_authenticated and user.is_user

def is_admin_user(user):
    return user.is_authenticated and user.is_admin

def home(request):
    return render(request,'home.html')

def adminclick(request):
    return  render(request,'adminclick.html')    

def studentclick(request):
    return  render(request,'studentclick.html')    

# ================  SignUpPages  ================================

def adminsignup(request):
    if request.method == 'POST':
        u = request.POST['u']
        f = request.POST['f']
        e = request.POST['e']
        p = request.POST['p']
        n = request.POST['n']
        if customuser.objects.filter(username=u).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return render(request, 'adminsignup.html')  # Render the form again
        user = customuser.objects.create_user(
            username=u,
            first_name=f,
            email=e,
            password=p,
            phone=n
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save()
        messages.success(request, 'Registration successful! Please login.')
        return redirect('adminlogin')
    return render(request, 'adminsignup.html')

def studentsignup(request):
    if request.method == 'POST':
        u = request.POST['u']
        f = request.POST['f']
        e = request.POST['e']
        p = request.POST['p']
        n = request.POST['n']
        branch = request.POST['branch']
        enrollment = request.POST['enrollment']
        if customuser.objects.filter(username=u).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return render(request, 'studentsignup.html')
        user = customuser.objects.create_user(
            username=u,
            first_name=f,
            email=e,
            password=p,
            phone=n,
            branch=branch,
            enrollment=enrollment,
        )
        if request.FILES.get('profile_pic'):
            user.profile_pic = request.FILES['profile_pic']
        user.is_user = True
        user.is_staff = True
        user.save()
        messages.success(request, 'Registration successful! Please login.')
        return redirect('studentlogin')
    return render(request, 'studentsignup.html')

# ============================ Admin Login ========================================

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('u')
        password = request.POST.get('p')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_admin:
                messages.success(request, 'Login successful. Welcome, ' + user.first_name + '!')
                return redirect('admindashboard')
            else:
                return redirect('login')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'adminlogin.html')

def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('u')
        password = request.POST.get('p')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_user:
                messages.success(request, 'Login successful. Welcome, ' + user.first_name + '!')
                return redirect('studentdashboard')
            else:
                return redirect('login')
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'studentlogin.html')

# ==================== Log out ===============================================================

def user_logout(request):
    if request.user.is_admin:
        logout(request)
        messages.success(request, 'Logout successful.')
        return redirect('adminlogin')
    elif request.user.is_user:
        logout(request)
        return redirect('studentlogin')
    logout(request)
    return redirect('home')



# ============================ Admin  Book Section =================================

@user_passes_test(is_admin_user)
@login_required(login_url='adminlogin')
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False) 
            book.is_active = True  
            book.save() 
            messages.success(request, 'Books Added Sucessfully')
            return redirect('view_books')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})

@user_passes_test(is_admin_user)
@login_required(login_url='adminlogin')
def view_books(request):
    books = Book.objects.all()
    issued_books = BookIssue.objects.filter(is_returned=False).values_list('book', flat=True)    
    books_info = []
    for book in books:
        is_issued = book.id in issued_books
        books_info.append({
            'book': book,
            'is_issued': is_issued
        }) 
    return render(request, 'view_books.html', {'books_info': books_info})


@user_passes_test(is_admin_user)
@login_required(login_url='adminlogin')
def update_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, 'Books Updated Sucessfully')
            print("Book saved:", book)  
            return redirect('view_books')
        else:
            print("Form errors:", form.errors)  
    else:
        form = BookForm(instance=book)
    print("Redirecting to update_book.html")  
    return render(request, 'update_book.html', {'form': form, 'book': book})

@user_passes_test(is_admin_user)
@login_required(login_url='adminlogin')
def delete_book(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        BookIssue.objects.filter(book=book).delete()
        book.delete()
        messages.success(request, 'Books Deleted Sucessfully')
    else:
        messages.error(request, 'Invalid request method.')
    return redirect('view_books')

def toggle_book_status(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.is_active:
        book.is_active = False
    else:
        book.is_active = True
    book.save()
    return redirect('view_books')  


# ============================ Student Book Views =======================

@login_required(login_url='studentlogin')
@user_passes_test(is_user)
def view_books1(request):
    books = Book.objects.all()      
    issued_books = BookIssue.objects.filter(student=request.user, is_returned=False).values_list('book', flat=True)
    all_issued_books = BookIssue.objects.filter(book__in=books, is_returned=False).values_list('book', flat=True)    
    books_info = []
    for book in books:
        is_issued = book.id in all_issued_books
        books_info.append({
            'book': book,
            'is_issued': is_issued
        })
    return render(request, 'view_books1.html', {'books_info': books_info})

# ============== Profile section =====================

@login_required(login_url='studentlogin')
@user_passes_test(is_user)
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

@login_required(login_url='studentlogin')
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', user.phone)
        user.enrollment = request.POST.get('enrollment', user.enrollment)
        branch_id = request.POST.get('branch')
        user.branch = Branch.objects.filter(id=branch_id).first() if branch_id else user.branch
        if request.FILES.get('profile_pic'):
            user.profile_pic = request.FILES['profile_pic']
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    branches = Branch.objects.all()
    return render(request, 'edit_profile.html', {'user': user, 'branches': branches})
@login_required(login_url='studentlogin')
def studentdashboard(request):
    return render(request, 'studentdashboard.html')


@login_required(login_url='studentlogin')
def view_my_issued_books(request):
    if request.method == 'POST':
        issue_id = request.POST.get('issue_id')
        action = request.POST.get('action')
        if action == 'return':
            book_issue = get_object_or_404(BookIssue, id=issue_id, student=request.user)
            if book_issue.is_returned:
                messages.warning(request, "This book has already been returned.")
            else:
                book_issue.is_returned = True
                book_issue.return_date = timezone.now().date()
                book_issue.save()
                messages.success(request, "Book returned successfully.")
            return redirect('view_my_issued_books')

        # Handle fine payment
        elif action == 'pay_fine':
            book_issue = get_object_or_404(BookIssue, id=issue_id, student=request.user)
            fine_amount = float(request.POST.get('fine_amount', 0))

            if fine_amount <= 0:
                messages.warning(request, "Invalid fine amount.")
            elif book_issue.fine_paid:
                messages.warning(request, "Fine has already been paid.")
            else:
                book_issue.fine_paid = True
                book_issue.save()
            return redirect('view_my_issued_books')

    issued_books = BookIssue.objects.filter(student=request.user, is_returned=False)
    for issue in issued_books:
        issue.fine = issue.calculate_fine()  # Calculate fine if not already done
        issue.save()  # Save the fine amount to the database
    current_date = timezone.now().date()  # Get the current date
    return render(request, 'view_my_issued_books.html', {
        'issued_books': issued_books,
        'current_date': current_date
    })


@login_required(login_url='studentlogin')
def pay_fine(request, issue_id):
    book_issue = get_object_or_404(BookIssue, id=issue_id, student=request.user)

    if request.method == 'POST':
        form = FinePaymentForm(request.POST, fine_amount=book_issue.fine)
        if form.is_valid():
            payment_method = form.cleaned_data['payment_method']
            account_number = form.cleaned_data.get('account_number')
            cvv = form.cleaned_data.get('cvv')
            # Assuming payment is successful
            book_issue.fine = 0 
            book_issue.fine_paid = True 
            book_issue.save()
            messages.success(request, 'Payment successful! Your fine has been cleared.')
            return redirect('view_my_issued_books')
    else:
        form = FinePaymentForm(fine_amount=book_issue.fine)
    return render(request, 'pay_fine.html', {'form': form, 'book_issue': book_issue})

@user_passes_test(is_admin_user)
@login_required(login_url='adminlogin')
def admindashboard(request):
    total_students = customuser.objects.filter(is_user=True).count()
    total_books =  Book.objects.filter(is_active=True,is_sold=False).count() 
    issued_books = BookIssue.objects.filter(is_returned=False).count()
    returned_books = BookIssue.objects.filter(is_returned=True).count()
    pending_requests = BookRequest.objects.filter(is_approved=False).count()  # Count of pending book requests
    return render(request, 'admindashboard.html', {
        'studentcount': total_students,
        'totalbooks': total_books,
        'issuedbooks': issued_books,
        'returnedbooks': returned_books,
        'pendingrequests': pending_requests,  
    })

# ===============   Admin Manage Student Section ==========================

@user_passes_test(is_admin_user)
@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Students Added SuccessFully')
            return redirect('list_students')
    else:
        form = StudentSignupForm()
    return render(request, 'add_student.html', {'form': form})

@user_passes_test(is_admin_user)
def list_students(request):
    students = customuser.objects.filter(is_user=True)  
    return render(request, 'list_students.html', {'students': students})

@user_passes_test(is_admin_user)
@login_required(login_url='adminlogin')
def update_student(request, student_id):
    student = get_object_or_404(customuser, id=student_id)
    if request.method == 'POST':
        student.first_name = request.POST.get('first_name', student.first_name)
        student.username = request.POST.get('u', student.username)
        student.email = request.POST.get('e', student.email)
        student.phone = request.POST.get('n', student.phone)
        branch_id = request.POST.get('branch')
        student.branch = Branch.objects.filter(id=branch_id).first()
        student.enrollment = request.POST.get('enrollment', student.enrollment)
        student.save()
        messages.success(request, 'Student Updated SucessFully !')
        return redirect('list_students')
    branches = Branch.objects.all()
    return render(request, 'update_student.html', {'student': student, 'branches': branches})

@user_passes_test(is_admin_user)
def delete_student(request, student_id):
    student = get_object_or_404(customuser, id=student_id)
    student.delete()
    messages.success(request, 'Student  Deleted Sucessfully !')
    return redirect('list_students')  

# =========================  Admin view Student Returned Book =======================

@user_passes_test(is_admin_user)
@login_required(login_url='adminlogin')
def students_who_returned_books(request):
    if request.method == 'POST':
        issue_id = request.POST.get('issue_id')
        book_issue = get_object_or_404(BookIssue, id=issue_id)
        if not book_issue.is_returned:
            book_issue.is_returned = True
            book_issue.return_date = timezone.now().date()
            book_issue.fine = book_issue.calculate_fine()  # Calculate fine before saving
            book_issue.save()
            messages.success(request, f'Book "{book_issue.book.name}" has been marked as returned.')
        return redirect('students_who_returned_books')
    book_issues = BookIssue.objects.all()
    student_book_info = []
    for issue in book_issues:
        student_book_info.append({
            'student': issue.student,
            'book': issue.book,
            'due_date': issue.due_date,
            'return_date': issue.return_date if issue.is_returned else 'Not Returned',
            'status': 'Returned' if issue.is_returned else 'Not Returned',
            'fine': issue.fine,
            'fine_paid': issue.fine_paid,
            'issue_id': issue.id
        })

    return render(request, 'students_who_returned_books.html', {'student_book_info': student_book_info})


# ===================== Issued Book  By Admin ================================

@login_required(login_url='adminlogin')
@user_passes_test(is_admin_user)
def issue_book(request):
    if request.method == 'POST':
        form = DiectBookIssueForm(request.POST)
        if form.is_valid():
            book_issue = form.save(commit=False)
            book = book_issue.book
            student = book_issue.student
            if BookIssue.objects.filter(book=book, is_returned=False).exists():
                form.add_error(None, 'This book is already issued.')
                return render(request, 'issue_book.html', {'form': form})
            if book.is_sold:
                form.add_error(None, 'This book is already sold.')
                return render(request, 'issue_book.html', {'form': form})
            book_issue.issue_date = timezone.now().date()
            book_issue.save()

            return redirect('view_issued_books')
    else:
        unsold_books = Book.objects.filter(is_sold=False)
        unissued_books = unsold_books.exclude(bookissue__is_returned=False)
        form = DiectBookIssueForm()   
        form.fields['book'].queryset = unissued_books  
        form.fields['student'].queryset = customuser.objects.filter(is_user=True)

    return render(request, 'issue_book.html', {'form': form})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin_user)
def view_issued_books(request):
    issued_books = BookIssue.objects.filter(book__is_active=True, book__is_sold=False).order_by('-issue_date')
    return render(request, 'view_issued_books.html', {'issued_books': issued_books})

# ======================= Student Check retuned Book ===============================

@login_required(login_url='studentlogin')
@user_passes_test(is_user)
def view_returned_books(request):
    returned_books = BookIssue.objects.filter(student=request.user, is_returned=True)
    return render(request, 'view_returned_books.html', {'returned_books': returned_books})

# ========================== Student Request Book ===========================

@login_required(login_url='studentlogin')
def request_book(request):
    if request.method == 'POST':
        form = BookRequestForm(request.POST)
        if form.is_valid():
            book_request = form.save(commit=False)
            if BookIssue.objects.filter(book=book_request.book, is_returned=False).exists():
                messages.error(request, 'This book is currently issued. You cannot request it right now.')
                issued_book_ids = list(BookIssue.objects.filter(is_returned=False).values_list('book_id', flat=True))
                return render(request, 'request_book.html', {'form': form, 'issued_book_ids': issued_book_ids})
            book_request.student = request.user
            book_request.save()
            return redirect('approval_message')
    else:
        available_books = Book.objects.filter(is_active=True, is_sold=False)
        form = BookRequestForm()
        form.fields['book'].queryset = available_books
    issued_book_ids = list(BookIssue.objects.filter(is_returned=False).values_list('book_id', flat=True))
    return render(request, 'request_book.html', {'form': form, 'issued_book_ids': issued_book_ids})

@login_required(login_url='studentlogin')
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    order_data = []
    for order in orders:
        books = [item.book for item in order.items.all()]
        estimated_delivery = order.created_at + timezone.timedelta(days=14)
        order_data.append({
            'order': order,
            'books': books,
            'estimated_delivery': estimated_delivery,
            'status': order.delivery_status,
        })
    return render(request, 'my_orders.html', {'order_data': order_data})


def approval_message(request):
    return render(request,'approval_message.html')

# ====================== Admin Manage  request Book ===============================

@user_passes_test(is_admin_user)
@login_required(login_url='adminlogin')
def view_book_requests(request):
    requests = BookRequest.objects.filter(is_approved=False)
    return render(request, 'view_book_requests.html', {'requests': requests})


def approve_request(request, request_id):
    book_request = get_object_or_404(BookRequest, id=request_id)
    if request.method == 'POST':
        form = DueDateForm(request.POST)
        if form.is_valid():
            due_date = form.cleaned_data['due_date']
            book_issue = BookIssue(
                student=book_request.student,
                book=book_request.book,
                issue_date=timezone.now().date(),
                due_date=due_date
            )
            book_issue.save()
            book_request.is_issued = True
            book_request.issued_date = timezone.now().date()
            book_request.save()
            book_request.delete()           
            return redirect('view_issued_books')  
    else:
        form = DueDateForm()

    return render(request, 'approve_request.html', {'form': form, 'book_request': book_request})

# ======================= Cart Section To Sold ========================

@login_required(login_url='studentlogin')
@user_passes_test(is_user)
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    issued_books = BookIssue.objects.filter(book=book, student=request.user, is_returned=False).exists()
    if not book.is_sold and not issued_books: 
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, 'Cart updated successfully!')
    return redirect('view_cart')

@login_required(login_url='studentlogin')
@user_passes_test(is_user)
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    for item in cart_items:
        book = item.book
        if BookIssue.objects.filter(book=book, student=request.user, is_returned=False).exists():
            item.delete()
            messages.success(request, 'Removed  updated successfully!')
    cart_items = cart.items.all() 
    total_price = sum(item.book.price * item.quantity for item in cart_items)
    return render(request, 'view_cart.html', {'cart': cart, 'total_price': total_price})


@login_required(login_url='studentlogin')
@user_passes_test(is_user)
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    if item.cart.user == request.user:
        item.delete()
        messages.success(request, 'Book removed from cart successfully.')
    return redirect('view_cart')

# ================= PayMent Section  =========================================

@login_required(login_url='studentlogin')
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    if request.method == 'POST':
        address = request.POST.get('address')
        cvv = request.POST.get('cvv')
        account_number = request.POST.get('account_number')
        if cart:
            total_price = sum(item.book.price * item.quantity for item in cart.items.all())
            order = Order.objects.create(
                user=request.user,
                account_number=account_number,
                address=address,
                cvv=cvv,
                total_price=total_price,
                created_at=timezone.now()
            )
            for item in cart.items.all():
                book = item.book
                book.is_sold = True
                book.sold_to = request.user
                book.save()
                OrderItem.objects.create(order=order, book=book)
            cart.items.all().delete()
            return render(request, 'transaction_details.html', {'order': order})
    total_price = sum(item.book.price * item.quantity for item in cart.items.all()) if cart else 0
    return render(request, 'checkout.html', {'cart': cart, 'total_price': total_price})


@login_required(login_url='studentlogin')
def transaction_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'transaction_details.html', {'order': order})

def download_transaction_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    estimated_delivery_date = order.created_at + timezone.timedelta(days=14)
    purchased_books = [item.book for item in order.items.all()]
    context = {
        'order': order,
        'estimated_delivery_date': estimated_delivery_date,
        'purchased_books': purchased_books,
    }
    from django.template.loader import get_template
    template = get_template('receipt_pdf.html')
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.CreatePDF(BytesIO(html.encode('UTF-8')), dest=result)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="receipt_order_{order_id}.pdf"'
        return response
    return HttpResponse('Error generating PDF', content_type='text/plain')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin_user)
def view_sold_books(request):
    sold_books = Book.objects.filter(is_sold=True)
    return render(request, 'view_sold_books.html', {'sold_books': sold_books})


# ==================== Order Tracking ====================

@user_passes_test(is_admin_user)
@login_required(login_url='adminlogin')
def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'admin_orders.html', {'orders': orders})


@user_passes_test(is_admin_user)
@login_required(login_url='adminlogin')
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        status = request.POST.get('delivery_status')
        order.delivery_status = status
        order.save()
        messages.success(request, f'Order #{order.id} status updated to {order.get_delivery_status_display()}.')
    return redirect('admin_orders')


# ==================== Branch Section ====================

@user_passes_test(is_admin_user)
@login_required(login_url='adminlogin')
def list_branches(request):
    branches = Branch.objects.all().order_by('-created_at')
    return render(request, 'list_branches.html', {'branches': branches})


@user_passes_test(is_admin_user)
@login_required(login_url='adminlogin')
def add_branch(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if Branch.objects.filter(name=name).exists():
            messages.error(request, 'Branch already exists.')
        else:
            Branch.objects.create(name=name)
            messages.success(request, 'Branch added successfully.')
            return redirect('list_branches')
    return render(request, 'add_branch.html')


@user_passes_test(is_admin_user)
@login_required(login_url='adminlogin')
def delete_branch(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)
    branch.delete()
    messages.success(request, 'Branch deleted successfully.')
    return redirect('list_branches')