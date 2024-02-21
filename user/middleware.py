from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status

class GoogleAuthenticationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("Middleware: Custom code is running!")
        request.foo = "bar"

        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        response = Response(
            data={
                "message": "Hello world"
            }, status=status.HTTP_200_OK
        )
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        return response