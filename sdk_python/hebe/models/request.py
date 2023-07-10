from pydantic import BaseModel, Field
from typing import Any, Optional
import uuid
from datetime import datetime, timezone
from uonet_request_signer_hebe import get_signature_values

APPLICATION_NAME: str = "DzienniczekPlus 2.0"
APPLICATION_VERSION: str = "1.4.2"
API_VERSION: int = 1
USER_AGENT = "Dart/2.10 (dart:io)"


class RequestPayload(BaseModel):
    application_name: str = Field(default=APPLICATION_NAME, alias="AppName")
    application_version: str = Field(default=APPLICATION_VERSION, alias="AppVersion")
    envelope: Any = Field(alias="Envelope")
    api: int = Field(default=API_VERSION, alias="API")
    request_id: str = Field(alias="RequestId", default=str(uuid.uuid4()))
    timestamp: str = Field(alias="Timestamp")
    timestamp_formatted: str = Field(alias="TimestampFormatted")
    firebase_token: Optional[str] = Field(alias="FirebaseToken")

    @staticmethod
    def build(envelope: Any, firebase_token: str = None) -> "RequestPayload":
        now: datetime = datetime.utcnow()
        return RequestPayload(
            envelope=envelope,
            timestamp=int(now.timestamp()),
            timestamp_formatted=now.strftime("%Y-%m-%d %H:%M:%S"),
            firebase_token=firebase_token,
        )

    class Config:
        allow_population_by_field_name = True


class RequestHeaders(BaseModel):
    user_agent: str = Field(alias="UserAgent", default=USER_AGENT)
    certificate_os: str = Field(alias="vOS")
    certificate_name: str = Field(alias="vDeviceModel")
    api_version: str = Field(alias="vAPI", default=str(API_VERSION))
    date: str = Field(alias="vDate")
    canonical_url: str = Field(alias="vCanonicalUrl")
    signature: str = Field(alias="Signature")
    digest: Optional[str] = Field(alias="Digest")
    content_type: Optional[str] = Field(alias="ContentType")

    @staticmethod
    def build(certificate, url: str, payload: Any = None):
        now: datetime = datetime.now(timezone.utc)
        digest, canonical_url, signature = get_signature_values(
            certificate.fingerprint, certificate.private_key, payload, url, now
        )
        return RequestHeaders(
            certificate_os=certificate.os,
            certificate_name=certificate.name,
            date=now.strftime("%a, %d %b %Y %H:%M:%S GMT"),
            canonical_url=canonical_url,
            signature=signature,
            digest=digest,
            content_type="application/json" if digest else None
        )

    class Config:
        allow_population_by_field_name = True
