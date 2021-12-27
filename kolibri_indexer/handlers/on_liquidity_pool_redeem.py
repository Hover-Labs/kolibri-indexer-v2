from decimal import Decimal

from dipdup.models import Transaction
from tortoise.exceptions import DoesNotExist

from kolibri_indexer.handlers.helpers import log_event
from kolibri_indexer.models import LiquidityPoolHolder, Event, LiquidityPoolHolderSnapshot
from kolibri_indexer.types.fa12_token.storage import Fa12TokenStorage
from dipdup.context import HandlerContext
from kolibri_indexer.types.liquidity_pool.parameter.redeem import RedeemParameter
from kolibri_indexer.types.fa12_token.parameter.transfer import TransferParameter
from kolibri_indexer.types.liquidity_pool.storage import LiquidityPoolStorage

async def on_liquidity_pool_redeem(
    _ctx: HandlerContext,
    redeem: Transaction[RedeemParameter, LiquidityPoolStorage],
    transfer: Transaction[TransferParameter, Fa12TokenStorage],
) -> None:
    assert redeem.data.sender_address == transfer.parameter.to, "Something's wrong with redeem attribution!"

    await log_event(
        redeem,
        Event.KolibriAction.LP_REDEEM,
        {
            'redeem_amt': redeem.parameter.__root__,
            'recv_kusd': transfer.parameter.value
        }
    )

    try:
        lp_holder = await LiquidityPoolHolder.get(address=redeem.data.sender_address)
        lp_holder.qlkusd_holdings -= Decimal(redeem.parameter.__root__)
        await lp_holder.save()
    except DoesNotExist:
        lp_holder = await LiquidityPoolHolder.create(address=redeem.data.sender_address,
                                                     qlkusd_holdings=Decimal(redeem.parameter.__root__))

    await LiquidityPoolHolderSnapshot.create(
        address=lp_holder.address,
        level=redeem.data.level,
        hash=redeem.data.hash,
        qlkusd_holdings=lp_holder.qlkusd_holdings,
    )

    print("Redeem! {} exchanged {:.4f} QLkUSD for {:.4f} kUSD".format(
        redeem.data.sender_address,
        Decimal(redeem.parameter.__root__) / Decimal(1e36),
        Decimal(transfer.parameter.value) / Decimal(1e18),
    ))
