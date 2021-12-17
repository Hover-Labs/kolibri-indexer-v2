from kolibri_indexer.models import KolibriOven
from kolibri_indexer.types.kolibri_oven.parameter.update_state import UpdateStateParameter
from dipdup.models import Transaction
from kolibri_indexer.types.kolibri_oven.storage import KolibriOvenStorage
from dipdup.context import HandlerContext

async def on_kolibri_oven_update_state(
    _ctx: HandlerContext,
    update_state: Transaction[UpdateStateParameter, KolibriOvenStorage],
) -> None:
    oven = await KolibriOven.get(address=update_state.data.target_address)

    oven.is_liquidated = update_state.parameter.bool
    oven.borrowed_tokens = update_state.parameter.nat
    oven.stability_fee_tokens = update_state.parameter.int_0
    oven.interest_index = update_state.parameter.int_1

    await oven.save()

    print("updateState called for {}".format(update_state.data.target_address))
