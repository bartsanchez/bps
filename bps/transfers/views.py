import hashlib
import logging

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

from .models import ProcessedBulkTransfer

logger = logging.getLogger(__name__)


@csrf_protect
@require_http_methods(["POST"])
async def bulk_transfer(request):
    content = request.body

    logger.info("Received content: %(content)", extra={"content": content.decode()})

    # Idempotency
    # Ensure we are not processing the same request more than once
    hashed_content = hashlib.sha256(content).hexdigest()
    query = ProcessedBulkTransfer.objects.filter(request_hash=hashed_content)
    already_processed = await query.aexists()
    if already_processed:
        return HttpResponse(status=422)

    # Store request
    await ProcessedBulkTransfer.objects.acreate(content=content.decode())

    return HttpResponse("OK")
