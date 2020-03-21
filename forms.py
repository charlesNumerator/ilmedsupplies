from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from wtforms.widgets import TextArea
import phonenumbers

style = {"style":"background:rgb(5, 36, 96) !important; color: white;"}

class ContactForm(FlaskForm):
    name = StringField('First Name: Last name optional.', [DataRequired()])
    email = StringField('Email:  To coordinate pickup of supplies.', [Email(message=('Not a valid email address.')), DataRequired()])
    phone = StringField('Phone: To coordinate pickup of supplies.', [DataRequired()])
    zip = StringField('Zip Code: Helps us figure out who can come pick up the supplies.', [DataRequired()])
    submit = SubmitField('Submit', render_kw=style)
    # recaptcha = RecaptchaField()

    def validate_phone(form, field):
        if len(field.data) > 16:
            raise ValidationError('Phone number is invalid.  Too long.')

        if len(field.data) < 9:
            raise ValidationError('Phone number must be at least 9 digits.')

        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            input_number = phonenumbers.parse("+1"+field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')

class OrgContactForm(FlaskForm):
    org_name = StringField('Organization Name', [DataRequired()])
    contact_name = StringField('Contact Name', [DataRequired()])
    email = StringField('Email', [Email(message=('Not a valid email address.')), DataRequired()])
    phone = StringField('Phone', [DataRequired()])
    zip = StringField('Zip', [DataRequired()])
    info = StringField('Info',  widget=TextArea())
    submit = SubmitField('Submit', render_kw=style)
    # recaptcha = RecaptchaField()

    def validate_phone(form, field):
        if len(field.data) > 16:
            raise ValidationError('Phone number is invalid.  Too long.')

        if len(field.data) < 9:
            raise ValidationError('Phone number must be at least 9 digits.')

        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            input_number = phonenumbers.parse("+1"+field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
