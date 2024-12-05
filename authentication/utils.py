from udemy_app_api.utils import get_file_path, sanitize_path_component


def get_upload_path_user(instance, filename):
    # Use the sanitize_path_component function to sanitize the username
    safe_username = sanitize_path_component(instance.username)

    folder = "users/"

    folder += f"{safe_username}"  # Use sanitized username example: users/johndoe
    type = "profile_pics"
    # Call get_file_path with the sanitized folder, type, and filename
    return get_file_path(folder, type, filename)


