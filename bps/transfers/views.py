import logging

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

logger = logging.getLogger(__name__)


@require_http_methods(["POST"])
async def bulk_transfer(request):
    content = request.body.decode()

    logger.info("Received content: %(content)", extra={"content": content})

    return HttpResponse("OK")
