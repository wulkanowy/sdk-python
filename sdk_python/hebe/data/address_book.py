from pydantic import BaseModel, Field
from enum import Enum
from uuid import UUID

from sdk_python.hebe.api import API
from sdk_python.hebe.data.pupil import Pupil
from sdk_python.hebe.error import InvalidResponseEnvelopeTypeException


class AddressBookEntryGroup(Enum):
    PUPIL = "U"
    GUARDIAN = "O"
    EMPLOYEE = "P"


class AddressBookEntry(BaseModel):
    global_key: UUID = Field(alias="GlobalKey")
    group: AddressBookEntryGroup = Field(alias="Group")
    name: str = Field(alias="Name")

    @staticmethod
    async def get(api: API, pupil: Pupil, **kwargs) -> list["AddressBookEntry"]:
        envelope, envelope_type = await api.get(
            entity="messagebox/addressbook",
            rest_url=pupil.unit.rest_url,
            box_global_key=pupil.message_box.global_key,
            **kwargs
        )
        if envelope_type != "IEnumerable`1":
            raise InvalidResponseEnvelopeTypeException()
        return [AddressBookEntry.parse_obj(address_book_entry) for address_book_entry in envelope]
