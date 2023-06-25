from .views import register,loginview,ProviderInfo

from django.urls import path

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('reg', register.as_view() ),
        # login by user name 
    path ('login',loginview.as_view()),
                # we need view provider front send id back returns info ->
    path ('ProviderInfo',ProviderInfo.as_view()),
]
