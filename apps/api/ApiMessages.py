import enum
from django.utils.translation import gettext as _


class CommonApiMessages(enum.Enum):
    data_sent_successfully = _('Data sent successfully!')


class UserApiMessages(enum.Enum):
    user_updated_successfully = _('User updated successfully!')
    user_register_successfully = _('User register successfully!')
    user_not_register = _('User not register!')
    login_successfully = _('Login successfully!')
    first_name_field_is_required = _('First name field is required.')
    last_name_field_is_required = _('Last name field is required.')
    gender_field_required = _('Gender field is required.')
    image_format_not_allowed = _('Image format not allowed.')
    username_field_is_required = _('Username field is required.')
    username_is_exist = _('Username is already exist.')
    email_field_is_required = _('Email field is required.')
    email_is_exist = _('Email is already exist.')
    email_is_not_exists = _('Email is not exist.')
    mobile_number_field_required = _('Mobile number field is required.')
    mobile_number_exist = _('Mobile number is already exist.')
    password_not_match = _('Password is not match.')
    password_field_is_required = _('Password field is required.')
    confirm_password_field_is_required = _('Confirm password field is required.')

