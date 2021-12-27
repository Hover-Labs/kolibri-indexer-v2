from kolibri_indexer.models import OvenFactory
from kolibri_indexer.types.kolibri_oven_factory.storage import KolibriOvenFactoryStorage
from dipdup.models import Origination
from dipdup.context import HandlerContext

async def on_oven_factory_deploy(
    _ctx: HandlerContext,
    kolibri_oven_factory_origination: Origination[KolibriOvenFactoryStorage],
) -> None:
    await OvenFactory.create(
        address=kolibri_oven_factory_origination.data.originated_contract_address,
        created=kolibri_oven_factory_origination.data.timestamp,
        initial_delegate=kolibri_oven_factory_origination.storage.initialDelegate
    )
    print("Created OvenFactory!")
