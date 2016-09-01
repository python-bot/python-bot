import json

from python_bot.common.webhook.handlers.base import BaseWebHookHandler

__all__ = ["DjangoFacebookAdapter"]


class DjangoFacebookAdapter(BaseWebHookHandler):
    def stop(self):
        # create urls and start to django
        pass

    def start(self):
        # create urls and start to django
        pass

    def create_view(self):
        that = self
        from django.http import HttpResponse
        from django.utils.decorators import method_decorator
        from django.views import generic
        from django.views.decorators.csrf import csrf_exempt

        class DjangoView(generic.View):
            def get(self, request, *args, **kwargs):
                if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
                    return HttpResponse(self.request.GET['hub.challenge'])
                else:
                    return HttpResponse('Error, invalid token')

            @method_decorator(csrf_exempt)
            def dispatch(self, request, *args, **kwargs):
                return generic.View.dispatch(self, request, *args, **kwargs)

            # Post function to handle Facebook messages
            def post(self, request, *args, **kwargs):
                # Converts the text payload into a python dictionary
                text = json.loads(self.request.body.decode('utf-8'))
                # Facebook recommends going through every entry since they might send
                # multiple messages in a single call during high load
                for entry in text['entry']:
                    for message in entry['messaging']:
                        pass
                        # TBD
                        # Check to make sure the received call is a message call
                        # This might be delivery, optin, postback for other events
                        # if 'message' in message and 'text' in message['message']:
                        #     # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                        #     # are sent as attachments and must be handled accordingly.
                        #     that.messenger.on_message(message['sender']['id'], message['message']['text'])
                        # elif "postback" in message and "payload" in message["postback"]:
                        #     post_facebook_message(message['sender']['id'], payload=message["postback"]['payload'])
                return HttpResponse()

        return DjangoView.as_view()
