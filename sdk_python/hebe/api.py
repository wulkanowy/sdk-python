from typing import Any, Optional, Union
from datetime import datetime, date
from aiohttp import ClientSession
from enum import Enum
from pydantic import BaseModel, Field
import json

from sdk_python.hebe.models.request import RequestHeaders, RequestPayload
from sdk_python.hebe.models.response import Response
from sdk_python.hebe.error import (
    InvalidResponseContentTypeException,
    InvalidResponseContentException,
    NotFoundEndpointException,
    FailedRequestException,
    InvalidSignatureValuesException,
    InvalidRequestEnvelopeStructure,
    InvalidRequestHeadersStructure,
    UnauthorizedCertificateException,
    InvalidTokenException,
    UsedTokenException,
    InvalidPINException,
    ExpiredTokenException,
    SDKException,
)


class FilterListType(Enum):
    BY_PUPIL = "byPupil"
    BY_ID = "byId"


class GETParams(BaseModel):
    mode: Optional[int] = Field(alias="mode")
    id: Optional[int] = Field(alias="id")
    pupil_id: Optional[int] = Field(alias="pupilId")
    period_id: Optional[int] = Field(alias="periodId")
    constituent_unit_id: Optional[int] = Field(alias="constituentId")
    day: Optional[date] = Field(alias="day")
    last_sync_date: Optional[datetime] = Field(alias="lastSyncDate")
    last_item_id: Optional[int] = Field(alias="lastId")
    page_size: Optional[int] = Field(alias="pageSize")
    from_: Optional[date] = Field(alias="from")

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            date: lambda date: date.isoformat(),
            datetime: lambda datetime: datetime.isoformat(),
        }


class API:
    def __init__(self, certificate):
        self._session = ClientSession()
        self.certificate = certificate

    async def request(
        self, method: str, url: str, envelope: Any = None, **kwargs
    ) -> tuple[Any, str]:
        payload: RequestPayload = (
            RequestPayload.get(envelope).json(by_alias=True)
            if method == "POST" and envelope != None
            else None
        )
        headers: RequestHeaders = RequestHeaders.get(
            self.certificate, url, payload
        ).dict(by_alias=True)
        if method == "GET":
            try:
                response = await self._session.get(url, headers=headers, **kwargs)
            except:
                raise FailedRequestException()
        else:
            try:
                response = await self._session.request(
                    method, url, data=payload, headers=headers, **kwargs
                )
            except:
                raise FailedRequestException()
        if response.status == 404:
            raise NotFoundEndpointException()
        if response.headers["Content-Type"] != "application/json; charset=utf-8":
            raise InvalidResponseContentTypeException
        try:
            response: Response = Response.parse_raw(await response.text())
        except:
            raise InvalidResponseContentException()
        self._check_response_status(response.status.code, response.status.message)
        return response.envelope, response.envelope_type

    async def get(
        self,
        entity: str,
        rest_url: str,
        deleted: bool = False,
        filter_list_type: FilterListType = None,
        **kwargs,
    ) -> tuple[Any, str]:
        url: str = f"{rest_url}/mobile/{entity}{'/deleted' if deleted else ''}{f'/{filter_list_type.value}' if filter_list_type else ''}"
        params: dict[str, Union[int, str]] = json.loads(
            GETParams(**kwargs).json(by_alias=True, exclude_none=True)
        )
        envelope, envelope_type = await self.request("GET", url, params=params)
        return envelope, envelope_type

    def _check_response_status(self, status_code: int, status_message: str):
        if status_code != 0:
            if status_code == 100 and ": " in status_message:
                raise InvalidSignatureValuesException()
            elif status_code == 101:
                raise InvalidRequestEnvelopeStructure()
            elif status_code == 102:
                raise InvalidRequestHeadersStructure()
            elif status_code == 108:
                raise UnauthorizedCertificateException()
            elif status_code == 200:
                raise InvalidTokenException()
            elif status_code == 201:
                raise UsedTokenException()
            elif status_code == 203:
                raise InvalidPINException()
            elif status_code == 204:
                raise ExpiredTokenException()
            else:
                raise SDKException(f"[{status_code}] {status_message}")

    async def __aexit__(self):
        await self.session.close()
