from decimal import Decimal

from dipdup.models import BigMapDiff, BigMapAction
from dipdup.context import HandlerContext
from kolibri_indexer.types.harbinger_normalizer.big_map.asset_map_value import AssetMapValue
from kolibri_indexer.types.harbinger_normalizer.big_map.asset_map_key import AssetMapKey

from kolibri_indexer.models import HarbingerPrice

async def on_normalizer_xtz_update(
    _ctx: HandlerContext,
    asset_map: BigMapDiff[AssetMapKey, AssetMapValue],
) -> None:
    if asset_map.action == BigMapAction.UPDATE_KEY and asset_map.key.__root__ == 'XTZ-USD':
        computed_price = Decimal(asset_map.value.computedPrice)

        print("Adding harbinger price at ${}".format(computed_price / Decimal(1e6)))
        await HarbingerPrice.create(
            level = asset_map.data.level,
            timestamp = asset_map.data.timestamp,
            last_update_time = asset_map.value.lastUpdateTime,
            computed_price = Decimal(asset_map.value.computedPrice),
            prices = asset_map.value.prices.dict(),
            volumes = asset_map.value.volumes.dict(),
        )
