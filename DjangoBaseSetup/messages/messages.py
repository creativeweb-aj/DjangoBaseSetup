import enum
from django.utils.translation import gettext as _


class MainMessages(enum.Enum):
    the = _('The')
    field_is_required = _('Field is required.')


class ValidationMessages(enum.Enum):
    # User form messages
    first_name_field_is_required = _('First name field is required.')
    last_name_field_is_required = _('Last name field is required.')
    email_field_is_required = _('Email field is required.')
    email_is_not_valid = _('Email is not valid.')
    email_is_already_exists = _('Email is already exist.')
    username_field_is_required = _('Username field is required.')
    username_is_not_valid = _('Username is not valid.')
    mobile_field_is_required = _('Mobile number field is required.')
    mobile_number_exist = _('Mobile number is exist.')
    mobile_number_minimum = _('Mobile number is minimum number required.')
    mobile_number_maximum = _('Mobile number is maximum number required.')
    email_is_not_exists = _('Email is not registered.')
    old_password_is_required = _('Old password is required.')
    old_password_is_not_correct = _('Old password is not correct.')
    OTP_field_is_required = _('OTP field is required.')
    password_field_is_required = _('Password field is required.')
    new_password_field_is_required = _('New password field is required.')
    password_should_contains_atleast_8_digits = _('New password should contains atleast 8 digits.')
    confirm_password_should_contains_at_least_8_digits = _('Confirm password should contains at least 8 digits.')
    password_must_contain_upperchar_lowerchar_specchar_numbers = _(
        'Password must contain upperchar lowerchar specchar numbers.')
    confirm_password_field_is_required = _('Confirm password field is required.')
    confirm_password_and_new_password_must_match = _('Confirm password and new password must match.')

    # Permission form messages
    title_field_is_required = _('Title field is required.')
    path_field_is_required = _('Path field is required.')
    segment_field_is_required = _('Segment field is required.')
    order_field_is_required = _('Order field is required.')
    icon_field_is_required = _('Icon field is required.')

    # Email form messages
    name_field_is_required = _('Name field is required.')
    subject_field_is_required = _('Subject field is required.')
    action_field_is_required = _('Action field is required.')
    email_body_field_is_required = _('Email body field is required.')

    # CMS form messages
    page_name_field_is_required = _('Page name field is required.')
    description_field_is_required = _('Description field is required.')
    page_title_field_is_required = _('Page title field is required.')

    # FAQ form messages
    question_field_is_required = _('Question field is required.')
    answer_field_is_required = _('Answer field is required.')


# Login App
class LoginMessages(enum.Enum):
    # Login view method messages
    you_are_now_logged_in = _('You are now logged in!')
    otp_sent_to_mobile = _('OTP sent to your mobile number')
    invalid_username_and_password = _('Invalid username and password.')

    # Logout view method messages
    you_are_now_logged_out = _('You are now logged out! ')

    # Forgot password view method messages
    subject = _('Password reset requested.')
    siteName = _('Admin Django')
    welcome_message = _('Welcome to admin django.')
    login_credentials_email_sent_successfully = _('Login credentials sent successfully.')
    forgot_password_email_sent_success = _(
        'An email has been sent to your inbox. To reset your password please follow the steps mentioned in the email.')
    email_not_sent = _('Email not sent.')
    email_not_registered = _('Your email is not registered.')

    # Password reset view method messages
    password_reset_successfully = _('Password reset successfully.')

    profile_update_successfully = _('Profile update successfully.')

    # Update password view method messages
    password_has_been_updated_successfully = _('Password has been updated successfully.')

    credentials = _('Login credentials.')


# CmsPages App
class CmsPageMessages(enum.Enum):
    # Page update
    cms_page_has_been_updated_successfully = _('Cms page has been updated successfully.')
    cms_page_has_been_added_successfully = _('Cms page has been added successfully.')


class FaqMessages(enum.Enum):
    # Page update
    faq_page_has_been_updated_successfully = _('Faq has been updated successfully.')
    faq_page_has_been_added_successfully = _('Faq has been added successfully.')
    faq_page_has_been_deleted_successfully = _('Faq page has been deleted successfully.')
    faq_deactivated = _('Faq has been deactivated successfully.')
    faq_activated = _('Faq has been activated successfully.')
    faq_deleted = _('Faq has been deleted successfully.')


# Languages App
class LanguageMessages(enum.Enum):
    # Language update
    languageUpdateSuccess = _('Language has been updated successfully.')


# Email templates App
class EmailTemplateMessages(enum.Enum):
    # Email add 
    email_template_has_been_added_successfully = _('Email template has been added successfully.')

    # Email update
    email_template_has_been_updated_successfully = _('Email template has been updated successfully.')


# settings App
class SettingMessages(enum.Enum):
    # settings Add 
    settings_page_has_been_added_successfully = _('Setting page has been added successfully.')

    # settings update
    setting_has_been_updated_successfully = _('Setting has been updated successfully.')
    setting_has_been_deleted_successfully = _('Setting has been deleted successfully.')


class UserMessages(enum.Enum):
    # users Add 
    user_has_been_added_successfully = _('User has been added successfully.')

    # users Update
    user_profile_has_been_updated_successfully = _('User profile has been updated successfully.')
    user_deactivated = _('User has been deactivated successfully.')
    user_activated = _('User has been activated successfully.')
    staff_deactivated = _('Staff has been deactivated successfully.')
    staff_activated = _('Staff has been activated successfully.')

    # UserApi Delete
    user_has_been_deleted_successfully = _('User has been deleted successfully.')

    # UserApi Password
    user_password_updated_successfully = _('User password updated successfully.')


class PermissionMessages(enum.Enum):
    # add acl management
    acl_has_been_added_successfully = _('Acl has been added successfully.')

    # update acl management
    acl_has_been_updated_successfully = _('Acl has been updated successfully.')
    acl_deactivated = _('Acl has been deactivated successfully.')
    acl_activated = _('Acl has been activated successfully.')

    # delete acl management
    acl_has_been_deleted_successfully = _('Acl has been deleted successfully.')
