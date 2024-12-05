from udemy_app_api.utils import get_file_path, sanitize_path_component


# def get_upload_path_order_thumbnail(instance, filename):
#     # Use the sanitize_path_component function to sanitize the username
#     safe_username = sanitize_path_component(instance.user)
#     safe_order_name = sanitize_path_component(instance.name)

#     folder = "users/"

#     folder += f"{safe_username}/orders/{safe_order_name}"  # Use sanitized username example: users/johndoe
#     type = "thumbnails"
#     # Call get_file_path with the sanitized folder, type, and filename example: users/johndoe/course/filename
#     return get_file_path(folder, type, filename)


# def get_upload_path_order_video(instance, filename):
#     # Use the sanitize_path_component function to sanitize the username
#     safe_username = sanitize_path_component(instance.user.username)
#     safe_order_name = sanitize_path_component(instance.name)

#     folder = "users/"

#     folder += f"{safe_username}/orders/{safe_order_name}"  # Use sanitized username example: users/johndoe
#     type = "videos"
#     # Call get_file_path with the sanitized folder, type, and filename example: users/johndoe/course/filename
#     return get_file_path(folder, type, filename)
