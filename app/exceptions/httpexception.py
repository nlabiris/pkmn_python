class HttpException(Exception):
    """Exception raised for HTTP errors.

    Attributes:
        errorcode -- Custom error code
        description -- Error description
    """

    def __init__(self, errorcode, description):
        self.errorcode = errorcode
        self.description = description
        super().__init__(self.description)

    def __str__(self):
        return self.description
