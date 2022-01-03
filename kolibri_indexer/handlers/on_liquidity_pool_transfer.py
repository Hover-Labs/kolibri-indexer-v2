from decimal import Decimal

from tortoise.exceptions import DoesNotExist

from kolibri_indexer.handlers.helpers import log_event
from kolibri_indexer.models import LiquidityPoolHolder, Event, TokenSnapshot
from kolibri_indexer.types.liquidity_pool.parameter.transfer import TransferParameter
from kolibri_indexer.types.liquidity_pool.storage import LiquidityPoolStorage
from dipdup.models import Transaction
from dipdup.context import HandlerContext

async def on_liquidity_pool_transfer(
    _ctx: HandlerContext,
    transfer: Transaction[TransferParameter, LiquidityPoolStorage],
) -> None:

    try:
        to_holder = await LiquidityPoolHolder.get(address=transfer.parameter.to)
    except DoesNotExist:
        to_holder = await LiquidityPoolHolder.create(address=transfer.parameter.to, qlkusd_holdings=Decimal(0))

    try:
        from_holder = await LiquidityPoolHolder.get(address=transfer.parameter.from_)
    except DoesNotExist:
        from_holder = await LiquidityPoolHolder.create(address=transfer.parameter.from_, qlkusd_holdings=Decimal(0))

    tx_value = Decimal(transfer.parameter.value)

    print("Processing transfer for {:0.2f} QLkUSD from {} to {}".format(
        tx_value / Decimal(1e36),
        from_holder.address,
        to_holder.address
    ))

    from_holder.qlkusd_holdings -= tx_value
    to_holder.qlkusd_holdings += tx_value

    await TokenSnapshot.create(
        type=TokenSnapshot.Contract.QLKUSD,
        address=to_holder.address,
        level=transfer.data.level,
        hash=transfer.data.hash,
        holdings=to_holder.qlkusd_holdings
    )

    await TokenSnapshot.create(
        type=TokenSnapshot.Contract.QLKUSD,
        address=to_holder.address,
        level=transfer.data.level,
        hash=transfer.data.hash,
        holdings=from_holder.qlkusd_holdings
    )

    await log_event(
        transfer,
        Event.KolibriAction.LP_TRANSFER,
        {
            'tx_value': transfer.parameter.value,
            'to': transfer.parameter.to,
            'from': transfer.parameter.from_,
        }
    )

    await to_holder.save()
    await from_holder.save()
