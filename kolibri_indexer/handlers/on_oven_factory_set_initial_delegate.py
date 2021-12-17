from kolibri_indexer.models import OvenFactory
from kolibri_indexer.types.kolibri_oven_factory.parameter.set_initial_delegate import SetInitialDelegateParameter
from dipdup.models import Transaction
from dipdup.context import HandlerContext
from kolibri_indexer.types.kolibri_oven_factory.storage import KolibriOvenFactoryStorage

async def on_oven_factory_set_initial_delegate(
    _ctx: HandlerContext,
    set_initial_delegate: Transaction[SetInitialDelegateParameter, KolibriOvenFactoryStorage],
) -> None:
    oven_factory = await OvenFactory.first()

    oven_factory.initial_delegate = set_initial_delegate.parameter.__root__

    await oven_factory.save()

    print("Updated oven factory initialDelegate to {}".format(oven_factory.initial_delegate))
