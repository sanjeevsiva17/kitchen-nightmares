from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from django.conf.urls import url
from django.urls import path
from task.consumers import AcceptTaskConsumer, DeclinedTaskConsumer

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket':
        AuthMiddlewareStack(
            URLRouter(
                [
                    path("dashboard/", AcceptTaskConsumer),
                    path("declined/", DeclinedTaskConsumer)
                ]
            )
    )
})
