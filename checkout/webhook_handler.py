from django.http import HttpResponse


class StripeWH_Handler:

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
            handles stripe events other than succeeded or failed
        """
        return HttpResponse(
            content=f'Unhandled received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
            handles stripe payment_intent.succeeded webhook
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
            handles stripe payment_intent.payment webhook
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
