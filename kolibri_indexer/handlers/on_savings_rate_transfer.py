from decimal import Decimal

from dipdup.context import HandlerContext
from dipdup.models import Transaction
from tortoise.exceptions import DoesNotExist

from kolibri_indexer.handlers.helpers import log_event
from kolibri_indexer.models import SavingsRateHolder, TokenSnapshot, Event
from kolibri_indexer.types.savings_rate.storage import SavingsRateStorage
from kolibri_indexer.types.savings_rate.parameter.transfer import TransferParameter

async def on_savings_rate_transfer(
    _ctx: HandlerContext,
    transfer: Transaction[TransferParameter, SavingsRateStorage],
) -> None:

    try:
        to_holder = await SavingsRateHolder.get(address=transfer.parameter.to)
    except DoesNotExist:
        to_holder = await SavingsRateHolder.create(address=transfer.parameter.to, ksr_holdings=Decimal(0))

    try:
        from_holder = await SavingsRateHolder.get(address=transfer.parameter.from_)
    except DoesNotExist:
        from_holder = await SavingsRateHolder.create(address=transfer.parameter.from_, ksr_holdings=Decimal(0))

    tx_value = Decimal(transfer.parameter.value)

    print("Processing transfer for {:0.2f} KSR from {} to {}".format(
        tx_value / Decimal(1e36),
        from_holder.address,
        to_holder.address
    ))

    from_holder.ksr_holdings -= tx_value
    to_holder.ksr_holdings += tx_value

    await TokenSnapshot.create(
        type=TokenSnapshot.Contract.KSR,
        address=to_holder.address,
        level=transfer.data.level,
        hash=transfer.data.hash,
        holdings=to_holder.ksr_holdings
    )

    await TokenSnapshot.create(
        type=TokenSnapshot.Contract.KSR,
        address=to_holder.address,
        level=transfer.data.level,
        hash=transfer.data.hash,
        holdings=from_holder.ksr_holdings
    )

    await log_event(
        transfer,
        Event.KolibriAction.SAVINGS_POOL_TRANSFER,
        {
            'tx_value': transfer.parameter.value,
            'to': transfer.parameter.to,
            'from': transfer.parameter.from_,
        }
    )

    await to_holder.save()
    await from_holder.save()
