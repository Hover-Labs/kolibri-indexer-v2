from decimal import Decimal

from dipdup.models import Transaction
from dipdup.context import HandlerContext
from tortoise.exceptions import DoesNotExist

from kolibri_indexer.handlers.helpers import log_event
from kolibri_indexer.models import Event, SavingsRateHolder, TokenSnapshot
from kolibri_indexer.types.savings_rate.parameter.deposit import DepositParameter
from kolibri_indexer.types.stability_fund.storage import StabilityFundStorage
from kolibri_indexer.types.savings_rate.parameter.mint import MintParameter
from kolibri_indexer.types.stability_fund.parameter.accrue_interest import AccrueInterestParameter
from kolibri_indexer.types.savings_rate.storage import SavingsRateStorage

async def on_savings_rate_deposit(
    _ctx: HandlerContext,
    deposit: Transaction[DepositParameter, SavingsRateStorage],
    accrue_interest: Transaction[AccrueInterestParameter, StabilityFundStorage],
    mint: Transaction[MintParameter, SavingsRateStorage],
) -> None:
    print("Deposited {:0.2f} kUSD into KSR.".format(Decimal(deposit.parameter.__root__) / Decimal('1e18')))
    print("Minted {:0.2f} KSR.".format(Decimal(mint.parameter.value) / Decimal('1e36')))
    print("Asked for {:0.2f} kUSD from stability fund.".format(Decimal(accrue_interest.parameter.__root__) / Decimal('1e18')))

    assert deposit.data.sender_address == mint.parameter.address, "Something's wrong with deposit attribution!"

    await log_event(accrue_interest, Event.KolibriAction.ACCRUE_INTEREST_CALL, {'amount': accrue_interest.parameter.__root__})

    await log_event(
        deposit,
        Event.KolibriAction.SAVINGS_POOL_DEPOSIT,
        {
            'deposit_amt': deposit.parameter.__root__,
            'ksr_minted': mint.parameter.value
        }
    )

    try:
        savings_rate_holder = await SavingsRateHolder.get(address=deposit.data.sender_address)
        savings_rate_holder.ksr_holdings += Decimal(mint.parameter.value)
        await savings_rate_holder.save()
    except DoesNotExist:
        savings_rate_holder = await SavingsRateHolder.create(address=deposit.data.sender_address,
                                                             ksr_holdings=Decimal(mint.parameter.value))

    await TokenSnapshot.create(
        type=TokenSnapshot.Contract.KSR,
        address=savings_rate_holder.address,
        level=deposit.data.level,
        hash=deposit.data.hash,
        holdings=savings_rate_holder.ksr_holdings,
    )

    print("Deposit! {} exchanged {:.4f} kUSD for {:.4f} KSR".format(
        deposit.data.sender_address,
        Decimal(deposit.parameter.__root__) / Decimal(1e18),
        Decimal(mint.parameter.value) / Decimal(1e36),
    ))
