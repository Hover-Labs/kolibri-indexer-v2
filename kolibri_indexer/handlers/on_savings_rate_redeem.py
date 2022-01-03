from decimal import Decimal

from tortoise.exceptions import DoesNotExist

from kolibri_indexer.handlers.helpers import log_event
from kolibri_indexer.models import Event, SavingsRateHolder, TokenSnapshot
from kolibri_indexer.types.savings_rate.storage import SavingsRateStorage
from kolibri_indexer.types.fa12_token.parameter.transfer import TransferParameter
from dipdup.context import HandlerContext
from kolibri_indexer.types.stability_fund.parameter.accrue_interest import AccrueInterestParameter
from kolibri_indexer.types.stability_fund.storage import StabilityFundStorage
from kolibri_indexer.types.fa12_token.storage import Fa12TokenStorage
from dipdup.models import Transaction
from kolibri_indexer.types.savings_rate.parameter.redeem import RedeemParameter

async def on_savings_rate_redeem(
    _ctx: HandlerContext,
    redeem: Transaction[RedeemParameter, SavingsRateStorage],
    accrue_interest: Transaction[AccrueInterestParameter, StabilityFundStorage],
    transfer: Transaction[TransferParameter, Fa12TokenStorage],
) -> None:
    assert redeem.data.sender_address == transfer.parameter.to, "Something's wrong with redeem attribution!"

    await log_event(accrue_interest, Event.KolibriAction.ACCRUE_INTEREST_CALL, {'amount': accrue_interest.parameter.__root__})

    await log_event(
        redeem,
        Event.KolibriAction.SAVINGS_POOL_REDEEM,
        {
            'redeem_amt': redeem.parameter.__root__,
            'recv_kusd': transfer.parameter.value
        }
    )

    try:
        ksr_holder = await SavingsRateHolder.get(address=redeem.data.sender_address)
        ksr_holder.ksr_holdings -= Decimal(redeem.parameter.__root__)
        await ksr_holder.save()
    except DoesNotExist:
        ksr_holder = await SavingsRateHolder.create(address=redeem.data.sender_address,
                                                   ksr_holdings=Decimal(redeem.parameter.__root__))

    await TokenSnapshot.create(
        type=TokenSnapshot.Contract.QLKUSD,
        address=ksr_holder.address,
        level=redeem.data.level,
        hash=redeem.data.hash,
        holdings=ksr_holder.ksr_holdings,
    )

    print("Redeem! {} exchanged {:.4f} KSR for {:.4f} kUSD".format(
        redeem.data.sender_address,
        Decimal(redeem.parameter.__root__) / Decimal(1e36),
        Decimal(transfer.parameter.value) / Decimal(1e18),
    ))
