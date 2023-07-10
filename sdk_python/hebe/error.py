class SDKException(Exception):
    pass


class InvalidResponseContentTypeException(SDKException):
    pass


class InvalidResponseContentException(SDKException):
    pass


class NotFoundEndpointException(SDKException):
    pass


class MethodNotAllowedException(SDKException):
    pass


class FailedRequestException(SDKException):
    pass


class InvalidResponseEnvelopeTypeException(SDKException):
    pass


class NoUnitSymbolException(SDKException):
    pass


class NoPermissionsException(SDKException):
    pass


class InvalidRequestEnvelopeStructure(SDKException):
    pass


class InvalidRequestHeadersStructure(SDKException):
    pass


class UnauthorizedCertificateException(SDKException):
    pass


class NotFoundEntityException(SDKException):
    pass


class UsedTokenException(SDKException):
    pass


class InvalidPINException(SDKException):
    pass


class ExpiredTokenException(SDKException):
    pass
