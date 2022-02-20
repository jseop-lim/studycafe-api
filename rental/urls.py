from django.urls import path
from rental.views import student_views, purchase_views, rent_views

app_name = 'rental'


urlpatterns = [
    path('students', student_views.StudentListView.as_view(), name='student-list'),
    path('students/<int:pk>', student_views.StudentDetailView.as_view(), name='student-detail'),
    path('students/<int:pk>/purchases', student_views.StudentPurchaseView.as_view(), name='student-purchase'),
    
    path('tickets', purchase_views.TicketListView.as_view(), name='ticket-list'),
    path('tickets/<int:pk>', purchase_views.TicketDetailView.as_view(), name='ticket-detail'),
    path('purchases', purchase_views.PurchaseListView.as_view(), name='purchase-list'),
    
    path('seats', rent_views.SeatListView.as_view(), name='seat-list'),
    path('seats/<int:pk>', rent_views.SeatDetailView.as_view(), name='seat-detail'),
]
