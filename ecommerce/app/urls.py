from django.urls import path

from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm

urlpatterns = [
    # Pass function - views.function | Pass class - views.class.as_view()
    path('', views.home),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    # A slug is a string that can only include characters, numbers, dashes, and underscores
    path('category/<slug:id>', views.CategoryView.as_view(), name="category"),
    path('category-title/<id>', views.CategoryTitle.as_view(), name="category-title"),
    path('product-detail/<int:id>', views.ProductDetail.as_view(), name="product-detail"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('address/', views.address, name="address"),
    path('update-address/<int:id>', views.updateAddress.as_view(), name="update-address"),

    path('add-to-cart/', views.add_to_cart, name="add-to-cart"),
    path('cart/', views.cart, name="cart"),
    path('wishlist/', views.wishlist, name="wishlist"),
    path('order/', views.order, name="order"),
    path('checkout/', views.checkOut.as_view(), name="checkout"),
    path('payment-done/', views.payment_done, name="payment-done"),
    path('search/', views.search, name="search"),
    # ajax
    path('modify-cart/', views.modify_cart),
    path('modify-wishlist/', views.modify_wishlist),
    
    # login authentication, only registration is using our own view function
    path('customer-registration/', views.CustomerRegistrationView.as_view(), name="customer-registration"),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name="login"),
    path('password-change/', auth_view.PasswordChangeView.as_view(template_name='app/password-change.html', form_class=MyPasswordChangeForm, success_url='/password-changed'), name="password-change"),
    path('password-changed/', auth_view.PasswordChangeDoneView.as_view(template_name="app/password-changed.html"), name="password-changed"),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),
    
    # reset password
    path('password_reset/', auth_view.PasswordResetView.as_view(template_name='app/password-reset.html', form_class=MyPasswordResetForm), name="password_reset"),
    path('password_reset_done/', auth_view.PasswordResetDoneView.as_view(template_name='app/password-reset-done.html'), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='app/password-reset-confirm.html', form_class=MySetPasswordForm), name="password_reset_confirm"),
    path('password_reset_complete/', auth_view.PasswordResetCompleteView.as_view(template_name='app/password-reset-complete.html'), name="password_reset_complete"),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# + static to declare media folder and its root to use resource inside media folder

admin.site.site_header = "Neel Dairy"
admin.site.site_title = "Neel Dairy"
admin.site.site_index_title = "Welcome to Neel Dairy Shop"