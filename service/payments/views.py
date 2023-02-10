import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, DetailView

from .models import Item


class HomePageView(TemplateView):
    template_name = 'home.html'


class StripeConfigView(View):

    @csrf_exempt
    def get(self, request):
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


class CreateCheckoutSession(View):

    @csrf_exempt
    def get(self, request, id):
        item_id = self.kwargs["id"]
        item = Item.objects.get(id=item_id)
        domain_url = 'http://127.0.0.1:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create session
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': item.price,
                            'product_data': {
                                'name': item.name
                            },
                        },
                        'quantity': 1,
                    },
                ],
                metadata={
                    "product_id": item.id
                }
            )
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)})


class ItemDetailView(DetailView):
    template_name = 'item_detail.html'
    model = Item
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY
        context['items'] = Item.objects.all()
        return context


class StripeWebhookView(View):

    @csrf_exempt
    def get(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)

        if event['type'] == 'checkout.session.completed':
            print('Payment was successful.')
        return HttpResponse(status=200)


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"
