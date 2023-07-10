import json
from typing import Any
from aiohttp import ClientSession

from sdk_python.hebe.models.request import RequestHeaders, RequestPayload
from sdk_python.hebe.models.response import Response
from sdk_python.hebe.error import (
    InvalidResponseContentTypeException,
    InvalidResponseContentException,
    InvalidResponseEnvelopeTypeException,
    NotFoundEndpointException,
    MethodNotAllowedException,
    FailedRequestException,
    NoPermissionsException,
    InvalidRequestEnvelopeStructure,
    InvalidRequestHeadersStructure,
    UnauthorizedCertificateException,
    NotFoundEntityException,
    UsedTokenException,
    InvalidPINException,
    ExpiredTokenException,
    SDKException,
    NoUnitSymbolException,
)

PAGE_SIZE: int = 1000


class API:
    def __init__(self, certificate, rest_url: str = None):
        self._certificate = certificate
        self._rest_url = rest_url or certificate.rest_url
        self._session = ClientSession()

    async def send_request(
        self, method: str, endpoint: str, **kwargs
    ) -> tuple[Any, str]:
        url: str = f"{self._rest_url}/mobile/{endpoint}"
        headers: RequestHeaders = RequestHeaders.build(
            self._certificate, url, json.dumps(kwargs.get("json")) if kwargs.get("json") else None
        )
        print(headers.dict(by_alias=True, exclude_none=True), kwargs.get("json"))
        try:
            response = await self._session.request(
                method,
                url,
                headers=headers.dict(by_alias=True, exclude_none=True),
                **kwargs,
            )
        except:
            raise FailedRequestException()
        print(response.history)
        if response.status == 404:
            raise NotFoundEndpointException()
        if response.status == 405:
            raise MethodNotAllowedException()
        if response.headers["Content-Type"] != "application/json; charset=utf-8":
            raise InvalidResponseContentTypeException()
        try:
            response = Response.parse_raw(await response.text())
        except:
            raise InvalidResponseContentException()
        print(response)
        self._check_response_status_code(response.status.code)
        return response.envelope, response.envelope_type

    async def post(self, endpoint: str, envelope: Any, **kwargs) -> tuple[Any, str]:
        payload: RequestPayload = RequestPayload.build(
            envelope, self._certificate.firebase_token
        )
        return await self.send_request(
            "POST", endpoint, json=payload.dict(by_alias=True, exclude_none=True), **kwargs
        )

    async def get(self, endpoint: str, **kwargs) -> tuple[Any, str]:
        return await self.send_request("GET", endpoint, **kwargs)

    async def get_all(self, endpoint: str, params: dict, **kwargs) -> list[Any]:
        data: list[Any] = []
        params["pageSize"]: int = PAGE_SIZE
        while True:
            print(endpoint, params)
            envelope, envelope_type = await self.get(endpoint, params=params, **kwargs)
            if envelope_type != "IEnumerable`1":
                raise InvalidResponseEnvelopeTypeException()
            data += envelope
            if len(envelope) != PAGE_SIZE:
                break
            params["lastId"]: int = envelope[-1]["Id"]
        return data

    @staticmethod
    def _check_response_status_code(status_code: int) -> None:
        if status_code == 0:
            return
        if status_code == 100:
            raise NoPermissionsException()
        if status_code == 101:
            raise InvalidRequestEnvelopeStructure()
        if status_code == 102:
            raise InvalidRequestHeadersStructure()
        if status_code == 104:
            raise NoUnitSymbolException()
        if status_code == 108:
            raise UnauthorizedCertificateException()
        if status_code == 200:
            raise NotFoundEntityException()
        if status_code == 201:
            raise UsedTokenException()
        if status_code == 203:
            raise InvalidPINException()
        if status_code == 204:
            raise ExpiredTokenException()
        raise SDKException(status_code)

    async def __aexit__(self):
        await self._session.close()
