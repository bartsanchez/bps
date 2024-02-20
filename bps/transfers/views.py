from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(["POST"])
async def bulk_transfer(request):
    return HttpResponse("OK")
