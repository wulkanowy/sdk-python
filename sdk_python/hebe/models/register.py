from pydantic import BaseModel, Field


class RegisterNewRequestEnvelope(BaseModel):
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
