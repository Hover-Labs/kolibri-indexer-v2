
from dipdup.models import Transaction
from dipdup.context import HandlerContext

from kolibri_indexer.handlers.helpers import log_event
from kolibri_indexer.models import Event
from kolibri_indexer.types.kolibri_oven.parameter.repay import RepayParameter
from kolibri_indexer.types.kolibri_oven.storage import KolibriOvenStorage

async def on_kolibri_oven_repay(
    _ctx: HandlerContext,
    repay: Transaction[RepayParameter, KolibriOvenStorage],
) -> None:
    event = await log_event(repay, Event.KolibriAction.OVEN_REPAY, {'params': repay.parameter.__root__, })
    print("Created event {} - OVEN_REPAY - {}".format(event.id, event.target))

