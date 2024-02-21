import hashlib
import json
import logging

import redis
from asgiref.sync import sync_to_async
from bank_accounts.models import BankAccount
from django.db import transaction
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from transfers.models import ProcessedBulkTransfer

from bank_account_transfers.serializers import BankAccountTransfersRequestSerializer

logger = logging.getLogger(__name__)

UNPROCESSABLE_CONTENT_STATUS_CODE = 422


@csrf_exempt
@require_http_methods(["POST"])
async def bulk_transfer(request):
    content = request.body

    logger.info("Received content: %(content)", extra={"content": content.decode()})

    serializer = await serialize_data(content)
    if not serializer.is_valid():
        return HttpResponse(status=UNPROCESSABLE_CONTENT_STATUS_CODE)

    bank_account, exists = await bank_account_exists(serializer.validated_data)
    if not exists:
        return HttpResponse(status=UNPROCESSABLE_CONTENT_STATUS_CODE)

    # Setup semaphore to avoid race conditions
    r = redis.Redis(host="redis_semaphore")
    # Using IBAN as key for semaphore to not block operations for different accounts
    with r.lock(bank_account.iban):
        already_processed = await is_already_processed(content)
        if already_processed:
            return HttpResponse(status=UNPROCESSABLE_CONTENT_STATUS_CODE)

        result = await perform_operations(serializer, bank_account, content)
        if not result:
            return HttpResponse(status=UNPROCESSABLE_CONTENT_STATUS_CODE)

    return HttpResponse("OK")


@sync_to_async
def perform_operations(serializer, bank_account, content):
    # Ensure that everything is done or nothing
    with transaction.atomic():
        requested_amount_cents = serializer.requested_amount_cents()
        if requested_amount_cents > bank_account.balance_cents:
            return False

        serializer.save()

        bank_account.balance_cents -= requested_amount_cents
        bank_account.save()

        mark_as_processed(content)

    return True


async def serialize_data(content):
    data = json.loads(content)
    return BankAccountTransfersRequestSerializer(data=data)


async def is_already_processed(content):
    # Idempotency
    # Ensure we are not processing the same request more than once
    hashed_content = hashlib.sha256(content).hexdigest()
    query = ProcessedBulkTransfer.objects.filter(request_hash=hashed_content)
    return await query.aexists()


async def bank_account_exists(validated_data):
    iban = validated_data["organization_iban"]
    bic = validated_data["organization_bic"]
    query = BankAccount.objects.filter(iban=iban, bic=bic)
    return await query.afirst(), await query.aexists()


def mark_as_processed(content):
    return ProcessedBulkTransfer.objects.create(content=content.decode())
