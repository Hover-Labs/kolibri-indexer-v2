from decimal import Decimal

from kolibri_indexer.handlers.helpers import log_event
from kolibri_indexer.models import Event, KolibriOven
from kolibri_indexer.types.kolibri_oven.parameter.withdraw import WithdrawParameter
from kolibri_indexer.types.kolibri_oven.storage import KolibriOvenStorage
from dipdup.models import Transaction
from dipdup.context import HandlerContext

async def on_kolibri_oven_withdraw(
    _ctx: HandlerContext,
    withdraw: Transaction[WithdrawParameter, KolibriOvenStorage],
) -> None:
    oven = await KolibriOven.get(address=withdraw.data.target_address)

    oven.tez_deposited -= Decimal(withdraw.parameter.__root__)

    await oven.save()
    event = await log_event(withdraw, Event.KolibriAction.OVEN_WITHDRAW, {'params': withdraw.parameter.__root__, })
    print("Created event {} - OVEN_WITHDRAW - {}".format(event.id, event.target))
