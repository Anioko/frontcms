from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import (
    PasswordField,
    StringField,
    SubmitField,
    SelectField,
    IntegerField,
    DecimalField,
    FloatField
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import (
    Email,
    EqualTo,
    InputRequired,
    Length,
)

from app import db
from app.models import Role, User


#####Payment Forms Starts #####

class ChangeUserEmailForm(FlaskForm):
    email = EmailField(
        'New email', validators=[InputRequired(),
                                 Length(1, 64),
                                 Email()])
    submit = SubmitField('Update email')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class ChangeAccountTypeForm(FlaskForm):
    role = QuerySelectField(
        'New account type',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(Role).order_by('permissions'))
    submit = SubmitField('Update role')


class InviteUserForm(FlaskForm):
    role = QuerySelectField(
        'Account type',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(Role).order_by('permissions'))
    first_name = StringField(
        'First name', validators=[InputRequired(),
                                  Length(1, 64)])
    last_name = StringField(
        'Last name', validators=[InputRequired(),
                                 Length(1, 64)])
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])
    submit = SubmitField('Invite')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class NewUserForm(InviteUserForm):
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            EqualTo('password2', 'Passwords must match.')
        ])
    password2 = PasswordField('Confirm password', validators=[InputRequired()])

    submit = SubmitField('Create')


#####User Forms Ends #####
#####Payment Forms Start #####

class PaymentSettingForm(FlaskForm):

    name = StringField("Stripe Public Key or Public Key",validators=[InputRequired()])
    display_name = StringField("Display Name")
    value = StringField("Value", validators=[InputRequired()])
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')

#####Payment Forms Ends #####

#####Payment Forms Start #####

class PricingPlanForm(FlaskForm):

    name = StringField("Free or Basic or Pro or Gold",validators=[InputRequired()])
    duration = IntegerField("Number of days. E.g: 30", validators=[InputRequired()])
    cost = DecimalField("Cost e.g 0.00")
    currency_symbol = StringField("symbol")
    submit = SubmitField('Submit')


#####Payment Forms Ends #####


#####Transactionfee Forms Start #####

class TransactionFeeForm(FlaskForm):

    provider_name = StringField("Stripe or Paystack",validators=[InputRequired()])
    local_fee = IntegerField("Local Fee's. E.g: 100", validators=[InputRequired()])
    european_fee = IntegerField("European Fee's. E.g: 100")
    international_fee = IntegerField("International Fee's. E.g: 100", validators=[InputRequired()])
    our_fee = IntegerField("Our fee. E.g: 100", validators=[InputRequired()])
    transfer_fee = DecimalField("Provider's money transfer fee. E.g: 100", validators=[InputRequired()])
    local_percentage = DecimalField("Local percentage per transaction e.g 1.50")
    european_percentage = DecimalField("European percentage per transaction e.g 1.50")
    international_percentage = DecimalField("International percentage per transaction e.g 1.50")
    our_percentage = DecimalField("Our percentage per transaction e.g 1.50")
    currency_symbol = StringField("Currency Symbol",validators=[InputRequired()])
    submit = SubmitField('Submit')


#####Payment Forms Ends #####
