from django.contrib import admin
from .models import customuser, Book, Order, BookIssue, BookRequest, BookIssueRequest, Cart, CartItem, Branch, OrderItem

admin.site.register(customuser)
admin.site.register(Book)
admin.site.register(Order)
admin.site.register(BookIssue)
admin.site.register(BookRequest)
admin.site.register(BookIssueRequest)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Branch)
admin.site.register(OrderItem)
