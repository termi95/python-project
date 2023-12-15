class LoginReq:
    login: str
    password: str

class RegisterReq(LoginReq):
    rePassword: str