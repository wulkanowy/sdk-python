from typing import Any
from aiohttp import ClientSession
from sdk_python.hebe.models.request import RequestHeaders, RequestPayload
from sdk_python.hebe.models.response import Response
from sdk_python.hebe.error import (
    InvalidResponseContentTypeException,
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


class API:
    def __init__(self, certificate):
        self._session = ClientSession()
        self.certificate = certificate

    async def request(self, method: str, url: str, envelope: Any = None, **kwargs):
        payload: RequestPayload = (
            RequestPayload.get(envelope).json(by_alias=True)
            if method == "POST" and envelope != None
            else None
        )
        headers: RequestHeaders = RequestHeaders.get(
            self.certificate, url, payload
        ).dict(by_alias=True)
        try:
            response = await self._session.request(
                method, url, data=payload, headers=headers, **kwargs
            )
        except:
            raise FailedRequestException()
        if response.headers["Content-Type"] != "application/json; charset=utf-8":
            raise InvalidResponseContentTypeException
        response: Response = Response.parse_raw(await response.text())
        self._check_response_status(response.status.code, response.status.message)
        return response.envelope, response.envelope_type

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
