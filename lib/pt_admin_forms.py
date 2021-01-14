from wtforms import form, fields, validators
from werkzeug.security import check_password_hash


class LoginForm(form.Form):
    login = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, _):
        user = self.get_user()

        if not user or not check_password_hash(user.password, self.password.data):
            raise validators.ValidationError(
                'Invalid user or password')

    def get_user(self):
        from lib.pt_models import User
        return User.select().where(User.login == self.login.data).first()


class RegistrationForm(form.Form):
    login = fields.StringField(validators=[validators.required()])
    email = fields.StringField()
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, _):
        from lib.pt_models import User
        if User.select().where(User.login == self.login.data).exists():
            raise validators.ValidationError('Duplicate username')
