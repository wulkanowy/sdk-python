class SDKException(Exception):
    pass


class InvalidResponseContentTypeException(SDKException):
    pass


class InvalidResponseContentException(SDKException):
    pass


class NotFoundEndpointException(SDKException):
    pass


class FailedRequestException(SDKException):
    pass


class InvalidResponseEnvelopeTypeException(SDKException):
    pass


class InvalidSignatureValuesException(SDKException):
    pass


class InvalidRequestEnvelopeStructure(SDKException):
    pass


class InvalidRequestHeadersStructure(SDKException):
    pass


class UnauthorizedCertificateException(SDKException):
    pass


class InvalidTokenException(SDKException):
    pass


class UsedTokenException(SDKException):
    pass


class InvalidPINException(SDKException):
    pass


class ExpiredTokenException(SDKException):
    pass
