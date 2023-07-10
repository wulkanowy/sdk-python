from pydantic import BaseModel, Field
from uonet_request_signer_hebe import generate_key_pair
from uuid import uuid5, NAMESPACE_X500
from sdk_python.hebe.api import API

from sdk_python.hebe.error import InvalidResponseEnvelopeTypeException
from sdk_python.hebe.utils import get_server_url_by_token

DEFAULT_NAME: str = "wulkanowy/sdk-python"
DEFAULT_TYPE: str = "X509"
DEFAULT_OS: str = "Android"


class RegisterCertificateRequestEnvelope(BaseModel):
    os: str = Field(alias="OS")
    name: str = Field(alias="DeviceModel")
    certificate_pem: str = Field(alias="Certificate")
    certificate_type: str = Field(alias="CertificateType")
    fingerprint: str = Field(alias="CertificateThumbprint")
    pin: str = Field(alias="PIN")
    token: str = Field(alias="SecurityToken")
    self_identifier: str = Field(alias="SelfIdentifier")

    class Config:
        allow_population_by_field_name = True


class Certificate(BaseModel):
    pem: str
    fingerprint: str
    private_key: str
    type: str
    os: str
    name: str
    rest_url: str = None
    login_id: int = None
    firebase_token: str = None

    @staticmethod
    def create(
        pem: str = None,
        fingerprint: str = None,
        private_key: str = None,
        type: str = DEFAULT_TYPE,
        os: str = DEFAULT_OS,
        name: str = DEFAULT_NAME,
    ) -> "Certificate":
        if not pem or not fingerprint or not private_key:
            pem, fingerprint, private_key = generate_key_pair()
            type = DEFAULT_TYPE
        return Certificate(
            pem=pem,
            fingerprint=fingerprint,
            private_key=private_key,
            type=type,
            os=os,
            name=name,
        )

    async def register(
        self,
        token: str,
        symbol: str,
        pin: str,
        firebase_token: str = None,
        server_url: str = None,
        self_identifier: str = None,
    ) -> None:
        if not server_url:
            server_url = await get_server_url_by_token(token)
        if not self_identifier:
            self_identifier = str(uuid5(NAMESPACE_X500, self.fingerprint))
        rest_url: str = f"{server_url}/{symbol.lower()}/api"
        request_envelope: RegisterCertificateRequestEnvelope = (
            RegisterCertificateRequestEnvelope(
                os=self.os,
                name=self.name,
                certificate_pem=self.pem,
                certificate_type=self.type,
                fingerprint=self.fingerprint,
                pin=pin,
                token=token.upper(),
                self_identifier=self_identifier,
            )
        )
        api: API = API(self, rest_url)
        response_envelope, response_envelope_type = await api.post(
            "register/new", request_envelope
        )
        if response_envelope_type != "AccountPayload":
            raise InvalidResponseEnvelopeTypeException()
        self.firebase_token: str = firebase_token
        self.rest_url: str = rest_url
        self.login_id: int = response_envelope["LoginId"]
