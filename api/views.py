from django.middleware.cache import CacheMiddleware
from django.utils.decorators import method_decorator, decorator_from_middleware_with_args
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
import hashlib


from api.task import send_request_task


def custom_cache_page(timeout, *, cache=None, key_prefix=None):
    """
    copy of cache_page decorator with custom behavior
    """

    res = decorator_from_middleware_with_args(CacheMiddleware)(
        page_timeout=timeout,
        cache_alias=cache,
        key_prefix=key_prefix,
    )
    return res


def custom_cache_page_decorator(func):
    def wrapper(request, *args, **kwargs):
        key = hashlib.sha256((str(request.headers)+str(request.data)+str(request.query_params)).encode()).hexdigest()
        if cache.get(key):
            return Response(200)
        else:
            cache.set(key, 5*60)
            return func(request, *args, **kwargs)

    return wrapper


class TestView(APIView):
    allowed_methods = ('GET', )

    @method_decorator(custom_cache_page_decorator)
    def get(self, request, *args, **kwargs):
        task = send_request_task.delay()
        return Response(200, headers={'X-Celery-ID': task.id})
