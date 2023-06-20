from .views import register,loginview

from django.urls import path

urlpatterns = [
   # path('admin/', admin.site.urls),
    path('reg', register.as_view() ),
        # login by user name 
    path ('login',loginview.as_view()),
    
]
