from django.urls import path
from .views import HomePageView, StripeConfigView, CreateCheckoutSession, CancelView, SuccessView, ItemDetailView, \
    StripeWebhookView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('config/', StripeConfigView.as_view()),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('buy/<id>', CreateCheckoutSession.as_view(), name='create-checkout-session'),
    path('item/<id>', ItemDetailView.as_view()),
    path('webhook/', StripeWebhookView.as_view())
]
