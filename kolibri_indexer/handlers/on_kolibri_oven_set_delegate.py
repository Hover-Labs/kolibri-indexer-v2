
from kolibri_indexer.types.kolibri_oven.parameter.set_delegate import SetDelegateParameter
from kolibri_indexer.types.kolibri_oven.storage import KolibriOvenStorage
from dipdup.models import Transaction
from dipdup.context import HandlerContext

async def on_kolibri_oven_set_delegate(
    ctx: HandlerContext,
    set_delegate: Transaction[SetDelegateParameter, KolibriOvenStorage],
) -> None:
    print("Set Delegate called!")
