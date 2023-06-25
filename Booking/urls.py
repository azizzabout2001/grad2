from .views import ListNewService,ListNewReservation,View_Provider_Booked_times,RecipientBookedServices,Rating_Serializer
from . import views
from django.urls import path
# for the provider page 
# we need : front sends -> id of the provider and category,all  -> (back responds) with all of the service info that he provides
# for the recipient page 
#  we need : front sends -> sevice category,all   -> (back responds) with all of the service info of that category 

urlpatterns = [
    # path(book),
    
    path('providebooked',View_Provider_Booked_times.as_view()),
    
    path ('setRating',views.ServiceRating.as_view()),
    path('viewNotification' ,views.NotificationViewSet.as_view()),
    # recipient -> 
    path ('ServiceByCategory',views.ServicesByCategory.as_view()),
    path ('allcategory', views.allcategory.as_view()),
    path ('alldomain', views.alldomain.as_view()),
    # past reservations
    path ('returnRecipintPastReservations',RecipientBookedServices.as_view() ),
    #future  ricipient
    path ('returnRecipintFutureReservations',views.RecipientFutureServices.as_view() ),
    # provider ->
    path ('ServiceProviderByCategory',views.ServicesProviderByCategory.as_view()),

    #path ('ProviderHistory'),
    #path ('Provider'),
    path('newService', ListNewService.as_view() ),
    path('newReservation', ListNewReservation.as_view() ), 
    path ('SearchInServiceInfo',views.SearchInServiceInfo.as_view()),
]
