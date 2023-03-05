from pydantic import BaseModel
from uonet_request_signer_hebe import generate_key_pair
from uuid import uuid5, NAMESPACE_X500
from sdk_python.hebe.api import API

from sdk_python.hebe.models.register import RegisterNewRequestEnvelope
from sdk_python.hebe.error import InvalidResponseEnvelopeTypeException
from sdk_python.hebe.utils import get_server_url_by_token

DEFAULT_NAME: str = "wulkanowy/sdk-python"
DEFAULT_TYPE: str = "X509"
DEFAULT_OS: str = "Android"


class Certificate(BaseModel):
    pem: str
    fingerprint: str
    private_key: str
    type: str
    os: str
    name: str
    rest_url: str = None

    @staticmethod
    def create(
        type: str = DEFAULT_TYPE, os: str = DEFAULT_OS, name: str = DEFAULT_NAME
    ) -> "Certificate":
        pem, fingerprint, private_key = generate_key_pair()
        return Certificate(
            pem=pem,
            fingerprint=fingerprint,
            private_key=private_key,
            type=type,
            os=os,
            name=name,
        )

    async def register(self, token: str, symbol: str, pin: str):
        server_url: str = await get_server_url_by_token(token)
        url: str = f"{server_url}/{symbol}/api/mobile/register/new"
        request_envelope: RegisterNewRequestEnvelope = RegisterNewRequestEnvelope(
            os=self.os,
            name=self.name,
            certificate_pem=self.pem,
            certificate_type=self.type,
            fingerprint=self.fingerprint,
            pin=pin,
            token=token,
            self_identifier=str(uuid5(NAMESPACE_X500, self.fingerprint)),
        )
        api = API(self)
        response_envelope, response_envelope_type = await api.request(
            "POST", url, request_envelope
        )
        if response_envelope_type != "AccountPayload":
            raise InvalidResponseEnvelopeTypeException()
        self.rest_url = f'{response_envelope["RestURL"]}/api'
