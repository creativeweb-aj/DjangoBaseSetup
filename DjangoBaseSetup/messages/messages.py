import enum
from django.utils.translation import gettext as _


# Form fields validation messages
class ValidationMessages(enum.Enum):
    # Form validation messages
    the = _('The')
    field_is_required = _('Field is required.')
    user_id_required = _('User id is required.')
    tokenIsNotValid = _('User token is not valid.')
    fieldIsRequired = _('User id and token is required.')
    mobile_number_field_required = _('The phone number field is required.')
    mobile_otp_required = _('Mobile OTP is required.')
    mobile_number_exist = _('The phone number is already exist.')
    mobile_number_minimum = _('The phone number must be ten digit.')
    mobile_number_maximum = _('The maximum twelve digit phone number is allowed.')
    userIsNotExist = _('The username is not exist.')
    mobileOtpNotMatch = _('Mobile OTP is not match.')
    mobileOtpIsExpire = _('Mobile OTP is expired.')
    userIsExist = _('The username is already exist.')
    the_password_field_is_required = _('The password field is required.')
    the_email_field_is_required = _('The email field is required.')
    the_email_is_not_valid = _('The email is not valid.')
    the_username_is_not_valid = _('The username is not valid.')
    the_email_is_not_exists = _('The email is not registered.')
    emailIsExist = _('The email is already exist.')
    the_new_password_field_is_required = _('The new password field is required.')
    the_new_password_should_contains_atleast_8_digits = _('The new password should contains at least 8 digits.')
    the_confirm_password_field_is_required = _('The confirm password field is required.')
    the_confirm_password_should_contains_at_least_8_digits = _(
        'The confirm password should contains at least 8 digits.')
    the_confirm_password_and_new_password_must_match = _('The confirm password and new password must match.')
    the_password_must_contain_upperchar_lowerchar_specchar_numbers = _(
        'The password must contain upperchar lowerchar specchar numbers.')
    the_old_password_is_required = _('The old password is required.')
    the_old_password_is_not_correct = _('The old password is not correct.')
    passNotMatch = _('The password is not match.')
    wrongCredentials = _('The credentials is not correct.')
    socialTypeRequired = _('The social type is required.')
    socialIdRequired = _('The social id is required.')
    the_profile_image_is_required = _('The profile image is required.')
    the_image_format_not_allowed = _('The image format not allowed.')
    the_forgot_password_otp_is_not_valid = _('The forgot password otp is not valid.')
    the_forgot_password_otp_field_is_required = _('The forgot password otp field is required.')
    full_name_required = _('Full name is required.')
    parent_id_required = _('Parent id is required.')
    mobile_number_required = _('Mobile number is required.')
    email_required = _('Email is required.')
    gender_required = _('Gender is required.')
    dob_required = _('Date of birth is required.')
    address_required = _('Address is required.')
    relationship_required = _('Relationship is required.')
    relationship_not_found = _('Relationship not found.')
    latitude_required = _('Latitude is required.')
    longitude_required = _('Longitude is required.')
    clinic_id_required = _('clinic id required.')
    # Patient validation messages
    the_gender_field_is_required = _('The gender field is required.')
    the_date_birth_field_is_required = _('The date of birth field is required.')

    MRD_NO_is_required = _('MRD NO is required.')
    MRD_NO_is_already_exist = _('MRD NO is already exists.')
    the_state_field_is_required = _('The state field is required.')
    the_zip_code_field_is_required = _('The zip_code field is required.')
    the_marital_field_is_required = _('The marital field is required.')
    the_blood_group_field_is_required = _('The blood group field is required.')
    the_height_field_is_required = _('The height field is required.')
    the_weight_field_is_required = _('The weight field is required.')
    the_children_field_is_required = _('The children field is required.')

    # Category validation messages
    the_category_field_is_required = _('The category field is required.')

    # Master validation messages
    the_service_field_is_required = _('The service field is required.')
    the_qualification_field_is_required = _('The qualification field is required.')
    the_service_type_is_required = _('The service type is required.')
    the_service_type_name_is_required = _('The service type name is required.')
    the_service_charge_category_field_is_required = _('The service charge category field is required.')
    the_establishment_type_field_is_required = _('The establishment type field is required.')
    the_speciality_name_field_is_required = _('The speciality name field is required.')
    the_expertise_name_field_is_required = _('The expertise name field is required.')
    the_symptoms_name_field_is_required = _('The symptoms name field is required.')
    the_degree_name_field_is_required = _('The degree name field is required.')
    the_coverage_name_field_is_required = _('The coverage name field is required.')

    # Cms_page validation messages
    the_page_name_field_is_required = _('The page name field is required.')
    the_page_title_field_is_required = _('The page title field is required.')
    the_description_field_is_required = _('The description field is required.')

    cms_pageExits = _('The page title is already exists.')

    # Language validation messages
    languageTitle = _('The language name field is required.')
    languageCode = _('The language code field is required.')
    languageFolder = _('"The folder code field is required.')

    # Email_page validation messages
    the_name_field_is_required = _('The name field is required.')
    the_subject_field_is_required = _('The subject field is required.')
    the_email_body_field_is_required = _('The email body field is required.')
    the_action_field_is_required = _('The action field is required.')

    # users validations messages
    the_user_name_field_is_required = _('The user name field is required.')
    the_first_name_field_is_required = _('The first name field is required.')
    the_phone_no_field_is_required = _('The phone no. field is required.')
    the_last_name_field_is_required = _('The last name field is required.')
    the_address1_field_is_required = _('The address1 field is required.')
    userEmailWrong = _('The email must be a valid email address.')

    # Permission messages
    the_title_field_is_required = _('The title field is required.')
    the_path_field_is_required = _('The path field is required.')
    the_segment_field_is_required = _('The segment field is required.')
    the_order_field_is_required = _('The order field is required.')
    the_icon_field_is_required = _('The icon field is required.')

    # Designation messages
    the_designation_field_is_required = _('The designation field is required.')

    # Staff Validation messages
    the_email_is_already_exists = _('The email is already exists.')
    the_phone_no_is_already_exists = _('The phone no. is already exists.')

    # Faq Validations messages
    the_question_field_is_required = _('The question field is required.')
    the_answer_field_is_required = _('The answer field is required.')

    # Setting Validations messages
    title_field_required = _('The title field is required.')
    key_field_required = _('The key field is required.')
    value_field_required = _('The value field is required.')
    input_field_required = _('The input field is required.')
    attachment_field_required = _('The attachment field is required.')
    title_already_exists = _('The title is already exists.')
    file_not_valid = _('This is not an valid image. Please upload a valid image.')

    # Pharmacy Management Validations Messages
    the_pharmacy_name_field_is_required = _('The pharmacy name is required.')
    the_cmo_registration_field_is_required = _('The cmo registration no is required.')
    the_payment_field_is_required = _('The payment is required.')
    the_commission_field_is_required = _('The commission is required.')
    the_opening_time_field_is_required = _('The opening time is required.')
    the_address2_field_is_required = _('The address2 field is required.')
    the_city_field_is_required = _('The city is required.')
    the_country_field_is_required = _('The country is required.')

    # Login Validations Messages
    the_OTP_field_is_required = _('The OTP field is required.')

    # Hospital Management Validation Messages
    the_website_url_field_is_required = _('The website url field is required.')
    the_hospital_name_field_is_required = _('The Hospital name field is required.')
    the_service_offered_field_is_required = _('The service offered field is required.')

    # Doctor Management Validation Messages
    the_full_name_field_is_required = _('The full name field is required.')
    the_Aadhar_card_number_field_is_required = _('The Aadhar card number field is required.')
    the_total_experience_field_is_required = _('The total experience field is required.')
    the_fees_field_is_required = _('The fees field is required.')

    # Diagnostic Management Validation Messages
    the_diagnostic_name_field_required = _('The Diagnostic name field is required')

    # Clinic Management Validation Messages
    the_clinic_name_field_required = _('The Clinic name field is required')

    # doctor adhar card
    the_aadhar_card_no_is_required = _('The adhar card no. field is required.')
    aadhar_card_no_exist = _('The adhar card no. is exist.')
    adhar_number_minimum = _('The adhar number must be 15 digits.')
    adhar_number_maximum = _('The maximum 15 digit adhar number is allowed.')

    the_mci_no_field_is_required = _('The mci number field is required.')
    mci_number_exist = _('The mci number is already exist.')
    mci_number_minimum = _('The mci number must be ten digit.')
    mci_number_maximum = _('The maximum twelve digit mci number is allowed.')

    # patient information
    patient_id_required = _('The patient_id is required')
    patient_phone_required = _('The patient phone required')
    additional_info_required = _('The additional info required')
    doctor_id_required = _('The doctor id required')
    hospital_id_required = _('The hospital id required')
    diagnostic_id_required = _('The diagnostic id required')
    pharmacy_id_required = _('The pharmacy id required')
    category_id_required = _('The category id required')
    booking_date_time_required = _('booking_date_time_required')
    payment_method_required = _('payment_method_required')

    # Booking slot
    id_required = _('The id is required')
    booking_type_required = _('The booking type is required')
    day_required = _('The day required')
    is_booking_doctor_required = _('The booking doctor required')

    # Favourite Slot

    type_required = _('Type is required.')
    is_favourite = _('favourite is required. ')


class ApiResponseMessage(enum.Enum):
    userCreatedSuccess = _('User created successfully.')
    userNotCreatedError = _('User not create.')
    userLoginSuccess = _('User login successfully.')
    userLoginError = _('Invalid credentials.')
    dataSentSuccess = _('Data successfully sent.')
    profile_deleted_successfully = _('Profile deleted successfully.')
    profile_updated_successfully = _('Profile updated successfully.')
    profile_not_found = _('Profile not found.')
    dataSentFail = _('Data not sent.')
    passwordChangedSuccess = _('User password changed successfully.')
    passwordChangedError = _('User password not change.')
    passwordResetSuccess = _('User password reset successfully.')
    passwordResetError = _('User password not reset.')
    emailSent = _('Email has been sent.')
    emailNotSent = _('Email has been not sent.')
    tokenIsNotValid = _('OTP is not valid.')
    otpFieldIsRequired = _('OTP is required.')
    userEditProfile = _('User Profile Successfully Updated.')
    profileAdded = _('Profile added successfully.')
    userEditProfileImage = _('User Profile Image Successfully Updated.')
    appointment_booked_successfully = _('Appointment booked successfully.')
    blog_liked_successfully = _('Blog liked successfully.')
    blog_unliked_successfully = _('Blog unliked successfully.')
    booking_slot_sent_successfully = _('Booking slot sent successfully.')
    added_to_favourite = _('Added to favourite.')
    removed_to_favourite = _('Removed from favourite.')
    transaction_id_added_successfully = _('Transaction Id added successfully.')
    transaction_id_not_added = _('Transaction Id not added.')


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

    # user Delete
    user_has_been_deleted_successfully = _('User has been deleted successfully.')

    # user Password 
    user_password_updated_successfully = _('User password updated successfully.')


class Permission(enum.Enum):
    # add acl management
    acl_has_been_added_successfully = _('Acl has been added successfully.')

    # update acl management
    acl_has_been_updated_successfully = _('Acl has been updated successfully.')
    acl_deactivated = _('Acl has been deactivated successfully.')
    acl_activated = _('Acl has been activated successfully.')

    # delete acl management
    acl_has_been_deleted_successfully = _('Acl has been deleted successfully.')


class PatientManagement(enum.Enum):
    patient_has_been_added_successfully = _('Patient has been added successfully.')
    patient_has_been_updated_successfully = _('Patient has been updated successfully.')
    patient_has_been_deleted_successfully = _('Patient has been deleted successfully.')
    patient_has_been_activated_successfully = _('Patient has been activated successfully.')
    patient_has_been_deactivated_successfully = _('Patient has been deactivated successfully.')
    Patient_has_been_changed_password_successfully = _('Patient has been changed password successfully.')


class ImageSliderManagement(enum.Enum):
    image_has_been_added_Successfully = _('Image has been added successfully.')
    image_has_been_deleted_Successfully = _('Image has been deleted successfully.')
    image_has_been_activated_successfully = _('image has been activated successfully')
    image_has_been_deactivated_successfully = _('image has been deactivated successfully')


class BlogManagement(enum.Enum):
    blog_has_been_added_Successfully = _('blog has been added successfully.')
    blog_has_been_deleted_Successfully = _('blog has been deleted successfully.')
    blog_has_been_activated_successfully = _('blog has been activated successfully')
    blog_has_been_deactivated_successfully = _('blog has been deactivated successfully')
    blog_has_been_updated_successfully = _('blog has been updated successfully')


class CategoryMessages(enum.Enum):
    category_has_been_added_successfully = _('Category has been added successfully.')
    category_has_been_updated_successfully = _('Category has been updated successfully.')
    category_has_been_deleted_successfully = _('Category has been deleted successfully.')
    category_has_been_activated_successfully = _('Category has been activated successfully.')
    category_has_been_deactivated_successfully = _('Category has been deactivated successfully.')


# Masters/service type views & service views
class ServiceMessage(enum.Enum):
    service_has_been_added_successfully = _('Service has been added successfully.')
    service_has_been_updated_successfully = _('Service has been updated successfully.')
    service_has_been_deleted_successfully = _('Service has been deleted successfully.')
    service_has_been_activated_successfully = _('Service has been activated successfully.')
    service_has_been_deactivated_successfully = _('Service has been deactivated successfully.')


class ClinicManagementMessages(enum.Enum):
    Clinic_has_been_added_successfully = _('Clinic has been added successfully.')
    Clinic_has_been_updated_successfully = _('Clinic has been updated successfully.')
    Clinic_has_been_activated_successfully = _('Clinic has been activated successfully.')
    Clinic_has_been_deactivated_successfully = _('Clinic has been deactivated successfully.')
    Clinic_has_been_deleted_successfully = _('Clinic has been deleted successfully.')
    Clinic_password_has_been_changed_successfully = _('clinic password has been changed.')


class DiagnosticManagementMessages(enum.Enum):
    diagnostic_has_been_added_successfully = _('Diagnostic has been added successfully.')
    diagnostic_has_been_updated_successfully = _('Diagnostic has been updated successfully.')
    diagnostic_has_been_activated_successfully = _('Diagnostic has been activated successfully.')
    diagnostic_has_been_deactivated_successfully = _('Diagnostic has been deactivated successfully.')
    diagnostic_has_been_deleted_successfully = _('Diagnostic has been deleted successfully.')
    diagnostic_password_has_been_changed_successfully = _('Diagnostic password has been changed successfully.')


class DoctorManagementMessages(enum.Enum):
    doctor_has_been_added_successfully = _('Doctor has been added successfully.')
    doctor_has_been_updated_successfully = _('Doctor has been updated successfully.')
    doctor_has_been_deleted_successfully = _('Doctor has been deleted successfully.')
    doctor_has_been_activated_successfully = _('Doctor has been activated successfully.')
    doctor_has_been_deactivated_successfully = _('Doctor has been deactivated successfully.')
    doctor_password_has_been_changed_successfully = _('Doctor password has been changed successfully.')


class HospitalsManagementMessages(enum.Enum):
    hospital_has_been_added_successfully = _('Hospital has been added successfully.')
    hospital_has_been_updated_successfully = _('Hospital has been updated successfully.')
    hospital_has_been_deleted_successfully = _('Hospital has been deleted successfully.')
    hospital_has_been_activated_successfully = _('Hospital has been activated successfully.')
    hospital_has_been_deactivated_successfully = _('Hospital has been deactivated successfully.')
    hospital_password_has_been_changed_successfully = _('Hospital password has been changed successfully.')


class MastersMessages(enum.Enum):
    # qualification views
    qualification_added_successfully = _('Qualification Added Successfully')
    qualification_edited_successfully = _('Qualification Edited Successfully')
    qualification_deactivated_successfully = _('Qualification Deactivated Successfully')
    qualification_activated_successfully = _('Qualification Activated Successfully')
    qualification_deleted_successfully = _('Qualification Deleted Successfully')


class PharmacyManagementMessages(enum.Enum):
    # views
    pharmacy_has_been_added_successfully = _('Pharmacy has been added successfully.')
    pharmacy_has_been_updated_successfully = _('Pharmacy has been updated successfully.')
    pharmacy_has_been_deleted_successfully = _('Pharmacy has been deleted successfully.')
    pharmacy_has_been_activated_successfully = _('Pharmacy has been activated successfully.')
    pharmacy_has_been_deactivated_successfully = _('Pharmacy has been deactivated successfully.')
    pharmacy_password_has_been_changed_successfully = _('Pharmacy password has been changed successfully.')


class TipsAndTweetManagementMessages(enum.Enum):
    tip_has_been_added_successfully = _('Tip has been added successfully.')
    tip_has_been_updated_successfully = _('Tip has been updateed successfully.')
    tip_has_been_deleted_successfully = _('Tip has been deleted successfully.')
    tip_has_been_activated_successfully = _('Tip has been activated successfully.')
    tip_has_been_deactivated_successfully = _('Tip has been deactivated successfully.')

    tweet_has_been_added_successfully = _('Tweet has been added successfully.')
    tweet_has_been_updated_successfully = _('Tweet has been updateed successfully.')
    tweet_has_been_deleted_successfully = _('Tweet has been deleted successfully.')
    tweet_has_been_activated_successfully = _('Tweet has been activated successfully.')
    tweet_has_been_deactivated_successfully = _('Tweet has been deactivated successfully.')


class TestimonialsMessages(enum.Enum):
    testimonials_has_been_added_successfully = _('Testimonials has been added successfully.')
    testimonials_has_been_updated_successfully = _('Testimonials has been updateed successfully.')
    testimonials_has_been_deleted_successfully = _('Testimonials has been deleted successfully.')
    testimonials_has_been_activated_successfully = _('Testimonials has been activated successfully.')
    testimonials_has_been_deactivated_successfully = _('Testimonials has been deactivated successfully.')
