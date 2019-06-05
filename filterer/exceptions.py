class FiltererException(Exception):
    def __init__(self, message):
        self.message = message


class InvalidKernelConvolutionDataError(FiltererException):
    def __init__(self, message, expression=None):
        super().__init__(message)
        self.expression = expression


class EmptyFieldError(FiltererException):
    def __init__(self, message):
        super().__init__(message)
