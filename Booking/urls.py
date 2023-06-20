from .views import ListNewService,ListNewReservation,View_Provider_Booked_times,RecipientBookedServices,Rating_Serializer
from . import views

from django.urls import path

urlpatterns = [
    # path(book),
    path('newService', ListNewService.as_view() ),
    path('newReservation', ListNewReservation.as_view() ), 
    path('providebooked',View_Provider_Booked_times.as_view()),
    path ('returnRecipintReservations',RecipientBookedServices.as_view() ),
    path ('setRating',views.ServiceRating.as_view()),
    path('viewNotification' ,views.NotificationViewSet.as_view())
    
]
