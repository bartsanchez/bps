import hashlib
import json
import logging

import redis
from bank_accounts.models import BankAccount
from bank_accounts.serializers import BankAccountSerializer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import ProcessedBulkTransfer

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["POST"])
async def bulk_transfer(request):
    content = request.body

    logger.info("Received content: %(content)", extra={"content": content.decode()})

    serializer = await serialize_data(content)
    if not serializer.is_valid():
        return HttpResponse(status=422)

    bank_account = await bank_account_exists(serializer.data)
    if not bank_account:
        return HttpResponse(status=422)

    # Setup semaphore to avoid race conditions
    r = redis.Redis(host="redis_semaphore")
    with r.lock(
        "replace-me-with-iban",
    ):  # TODO: replace lock key with iban to allow requests from different accounts
        already_processed = await is_already_processed(content)
        if already_processed:
            return HttpResponse(status=422)

        await mark_as_processed(content)

    return HttpResponse("OK")


async def serialize_data(content):
    data = json.loads(content)
    return BankAccountSerializer(data=data)


async def is_already_processed(content):
    # Idempotency
    # Ensure we are not processing the same request more than once
    hashed_content = hashlib.sha256(content).hexdigest()
    query = ProcessedBulkTransfer.objects.filter(request_hash=hashed_content)
    return await query.aexists()


async def bank_account_exists(data):
    iban = data["organization_iban"]
    bic = data["organization_bic"]
    query = BankAccount.objects.filter(iban=iban, bic=bic)
    return await query.aexists()


async def mark_as_processed(content):
    return await ProcessedBulkTransfer.objects.acreate(content=content.decode())
