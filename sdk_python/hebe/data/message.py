from pydantic import BaseModel, Field, root_validator
from datetime import datetime
from typing import Optional
from enum import Enum
from uuid import UUID

from sdk_python.hebe.api import API, FilterListType
from sdk_python.hebe.data.pupil import Pupil
from sdk_python.hebe.error import InvalidResponseEnvelopeTypeException
from sdk_python.hebe.models.attachment import Attachment


class Folder(Enum):
    INBOX = 1
    OUTBOX = 2
    DELETED = 3


class MessageAddressAdditionalInfos(BaseModel):
    team: Optional[str] = Field(alias="DisplayedClass")


class MessageAddress(BaseModel):
    global_key: UUID = Field(alias="GlobalKey")
    name: str = Field(alias="Name")
    has_read: Optional[bool] = Field(alias="HasRead")
    additional_infos: Optional[MessageAddressAdditionalInfos] = Field(alias="Extras")


class Message(BaseModel):
    id: UUID = Field(alias="Id")
    global_key: UUID = Field(alias="GlobalKey")
    thread_key: UUID = Field(alias="ThreadKey")
    subject: str = Field(alias="Subject")
    sender: MessageAddress = Field(alias="Sender")
    date_sent: datetime = Field(alias="DateSent")
    receiver: list[MessageAddress] = Field(alias="Receiver")
    date_read: Optional[datetime] = Field(alias="DateRead")
    importance: bool = Field(alias="Importance")
    content: str = Field(alias="Content")
    attachments: list[Attachment] = Field(alias="Attachments")

    @root_validator(pre=True)
    def root_validator(cls, values):
        values["GlobalKey"] = UUID(values["GlobalKey"])
        values["ThreadKey"] = UUID(values["ThreadKey"])
        values["DateSent"] = datetime.fromtimestamp(
            values["DateSent"]["Timestamp"] / 1000
        )
        values["DateRead"] = (
            datetime.fromtimestamp(values["DateRead"]["Timestamp"] / 1000)
            if values["DateRead"]
            else None
        )
        return values

    @staticmethod
    async def get_by_box(api: API, pupil: Pupil, folder: Folder, **kwargs) -> list["Message"]:
        envelope, envelope_type = await api.get(
            entity="messagebox/message",
            rest_url=pupil.unit.rest_url,
            filter_list_type=FilterListType.BY_BOX,
            folder=folder.value,
            box_global_key=pupil.message_box.global_key,
            **kwargs
        )
        if envelope_type != "IEnumerable`1":
            raise InvalidResponseEnvelopeTypeException()
        return [Message.parse_obj(message) for message in envelope]
