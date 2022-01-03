from decimal import Decimal

from dipdup.context import HandlerContext
from tortoise.exceptions import DoesNotExist

from kolibri_indexer.handlers.helpers import log_event
from kolibri_indexer.models import LiquidityPoolHolder, Event, TokenSnapshot
from kolibri_indexer.types.liquidity_pool.storage import LiquidityPoolStorage
from dipdup.models import Transaction
from kolibri_indexer.types.liquidity_pool.parameter.mint import MintParameter
from kolibri_indexer.types.liquidity_pool.parameter.deposit import DepositParameter

async def on_liquidity_pool_deposit(
    _ctx: HandlerContext,
    deposit: Transaction[DepositParameter, LiquidityPoolStorage],
    mint: Transaction[MintParameter, LiquidityPoolStorage],
) -> None:
    assert deposit.data.sender_address == mint.parameter.address, "Something's wrong with deposit attribution!"

    await log_event(
        deposit,
        Event.KolibriAction.LP_DEPOSIT,
        {
            'deposit_amt': deposit.parameter.__root__,
            'qlkusd_minted': mint.parameter.value
        }
    )

    try:
        lp_holder = await LiquidityPoolHolder.get(address=deposit.data.sender_address)
        lp_holder.qlkusd_holdings += Decimal(mint.parameter.value)
        await lp_holder.save()
    except DoesNotExist:
        lp_holder = await LiquidityPoolHolder.create(address=deposit.data.sender_address,
                                                     qlkusd_holdings=Decimal(mint.parameter.value))

    await TokenSnapshot.create(
        type=TokenSnapshot.Contract.QLKUSD,
        address=lp_holder.address,
        level=deposit.data.level,
        hash=deposit.data.hash,
        holdings=lp_holder.qlkusd_holdings,
    )

    print("Deposit! {} exchanged {:.4f} kUSD for {:.4f} QLkUSD".format(
        deposit.data.sender_address,
        Decimal(deposit.parameter.__root__) / Decimal(1e18),
        Decimal(mint.parameter.value) / Decimal(1e36),
    ))
