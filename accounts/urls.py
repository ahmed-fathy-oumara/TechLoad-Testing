from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='sign_up'),
    path('login/', views.login, name='sign_in'),
    path('logout/', views.logout, name='sign_out'),
    
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    
    path('user-info', views.profileInfo, name='profile_info'),
    path('user-downloads', views.profileDownloads, name='profile_downloads'),
    path('user-security', views.profileSecurity, name='profile_security'),
    path('user-help-center', views.profileHelpCenter, name='profile_help_center'),
    
    # path('user-dashboard', views.profileDashboard, name='profile_dashboard'),
    # path('user-notifications', views.profileNotifications, name='profileـnotifications'),
    # path('user-reviews', views.profileReviews, name='profileـreviews'),
    # path('user-offers', views.profileOffers, name='profile_offers'),
    # path('user-extended-offers', views.profileExtendedOffers, name='profile_extended_offers'),
    # path('user-settings', views.profileSettings, name='profile_settings'),
]
