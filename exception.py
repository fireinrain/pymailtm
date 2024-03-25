class TmBaseException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        print("%s: %s" % (self.code, self.message))

    @staticmethod
    def check_result_status(code: int):
        if code == 200 or code == 204:
            return
        if code == 400:
            raise BadRequestException()
        if code == 401:
            raise UnauthorizedException()
        if code == 404:
            raise NotFoundException()
        if code == 405:
            raise MethodNotAllowed()
        if code == 418:
            raise TeaPotException()
        if code == 422:
            raise UnprocessableException()
        if code == 429:
            raise TooManyRequestsException()


class BadRequestException(TmBaseException):
    def __init__(self):
        self.code = 400
        self.message = "Bad request 400: Something in your payload is missing! Or, the payload isn't there at all."


class UnauthorizedException(TmBaseException):
    def __init__(self):
        self.code = 401
        self.message = "Your token isn't correct (Or the headers hasn't a token at all!)."


class NotFoundException(TmBaseException):
    def __init__(self):
        self.code = 404
        self.message = "You're trying to access an account that doesn't exist? Or maybe reading a non-existing message"


class MethodNotAllowed(TmBaseException):
    def __init__(self):
        self.code = 405
        self.message = "Method not allowed 405: Maybe you're trying to GET a /token or POST a /messages"


class TeaPotException(TmBaseException):
    def __init__(self):
        self.code = 418
        self.message = "I'm a teapot 418: Who knows? Maybe the server becomes a teapot!"


class UnprocessableException(TmBaseException):
    def __init__(self):
        self.code = 422
        self.message = ("Some went wrong on your payload. Like, the username of the address while creating the account "
                        "isn't long enough, or, the account's domain isn't correct.")


class TooManyRequestsException(TmBaseException):
    def __init__(self):
        self.code = 429
        self.message = "You exceeded the limit of 8 requests per second! Try delaying the request by one second!"
