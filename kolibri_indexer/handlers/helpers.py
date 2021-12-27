from typing import Union

from dipdup.models import Transaction, Origination

from kolibri_indexer.models import Event

async def log_event(item: Union[Transaction, Origination], action: Event.KolibriAction, additional_data: dict):
    return await Event.create(
        sender=item.data.sender_address,
        target=item.data.target_address,
        level=item.data.level,
        initiator=item.data.initiator_address,
        action=action,
        timestamp=item.data.timestamp,
        data={
            'sender_alias': item.data.sender_alias,
            'target_alias': item.data.target_alias,
            'initiator_alias': item.data.initiator_alias
        } | additional_data,
    )
