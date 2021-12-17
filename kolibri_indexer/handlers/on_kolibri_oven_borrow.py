
from dipdup.models import Transaction
from dipdup.context import HandlerContext

from kolibri_indexer.handlers.helpers import log_event
from kolibri_indexer.models import Event
from kolibri_indexer.types.kolibri_oven.parameter.borrow import BorrowParameter
from kolibri_indexer.types.kolibri_oven.storage import KolibriOvenStorage

async def on_kolibri_oven_borrow(
    _ctx: HandlerContext,
    borrow: Transaction[BorrowParameter, KolibriOvenStorage],
) -> None:
    event = await log_event(borrow, Event.KolibriAction.OVEN_BORROW, {'params': borrow.parameter.__root__, })

    print("Created event {} - OVEN_BORROW - {}".format(event.id, event.target))
