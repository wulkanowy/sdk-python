class SDKException(Exception):
    pass


class InvalidResponseContentTypeException(BaseException):
    pass


class FailedRequestException(BaseException):
    pass


class InvalidResponseEnvelopeTypeException(BaseException):
    pass


class InvalidSignatureValuesException(BaseException):
    pass


class InvalidRequestEnvelopeStructure(BaseException):
    pass


class InvalidRequestHeadersStructure(BaseException):
    pass


class UnauthorizedCertificateException(BaseException):
    pass


class InvalidTokenException(BaseException):
    pass


class UsedTokenException(BaseException):
    pass


class InvalidPINException(BaseException):
    pass


class ExpiredTokenException(BaseException):
    pass
