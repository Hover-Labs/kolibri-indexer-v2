from decimal import Decimal

from dipdup.models import Transaction
from dipdup.context import HandlerContext
from tortoise.exceptions import DoesNotExist

from kolibri_indexer.handlers.helpers import log_event
from kolibri_indexer.models import kUSDHolder, Event, TokenSnapshot
from kolibri_indexer.types.fa12_token.storage import Fa12TokenStorage
from kolibri_indexer.types.fa12_token.parameter.transfer import TransferParameter

async def on_kusd_transfer(
    _ctx: HandlerContext,
    transfer: Transaction[TransferParameter, Fa12TokenStorage],
) -> None:

    try:
        to_holder = await kUSDHolder.get(address=transfer.parameter.to)
    except DoesNotExist:
        to_holder = await kUSDHolder.create(address=transfer.parameter.to, kusd_holdings=Decimal(0))

    try:
        from_holder = await kUSDHolder.get(address=transfer.parameter.from_)
    except DoesNotExist:
        from_holder = await kUSDHolder.create(address=transfer.parameter.from_, kusd_holdings=Decimal(0))

    tx_value = Decimal(transfer.parameter.value)

    print("Processing transfer for {:0.2f} kUSD from {} to {}".format(
        tx_value / Decimal(1e18),
        from_holder.address,
        to_holder.address
    ))

    from_holder.kusd_holdings -= tx_value
    to_holder.kusd_holdings += tx_value

    await TokenSnapshot.create(
        type=TokenSnapshot.Contract.KUSD,
        address=to_holder.address,
        level=transfer.data.level,
        hash=transfer.data.hash,
        holdings=to_holder.kusd_holdings
    )
    await TokenSnapshot.create(
        type=TokenSnapshot.Contract.KUSD,
        address=to_holder.address,
        level=transfer.data.level,
        hash=transfer.data.hash,
        holdings=from_holder.kusd_holdings
    )

    await log_event(
        transfer,
        Event.KolibriAction.KUSD_TRANSFER,
        {
            'tx_value': transfer.parameter.value,
            'to': transfer.parameter.to,
            'from': transfer.parameter.from_,
        }
    )

    await to_holder.save()
    await from_holder.save()
