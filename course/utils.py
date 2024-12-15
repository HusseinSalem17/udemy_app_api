from udemy_app_api.utils import get_file_path, sanitize_path_component


def get_upload_path_course_thumbnail(instance, filename):
    # Use the sanitize_path_component function to sanitize the username
    safe_username = sanitize_path_component(instance.teacher.username)
    safe_course_name = sanitize_path_component(instance.name)

    folder = "users/"

    folder += f"{safe_username}/{safe_course_name}"  # Use sanitized username example: users/johndoe
    type = "thumbnails"
    # Call get_file_path with the sanitized folder, type, and filename example: users/johndoe/course/filename
    return get_file_path(folder, type, filename)


def get_upload_path_course_videos(instance, filename):
    # Use the sanitize_path_component function to sanitize the username
    safe_username = sanitize_path_component(instance.course.teacher.username)
    safe_course_name = sanitize_path_component(instance.course.name)

    folder = "users/"

    folder += f"{safe_username}/{safe_course_name}"  # Use sanitized username example: users/johndoe
    type = "videos"
    # Call get_file_path with the sanitized folder, type, and filename example: users/johndoe/course/filename
    return get_file_path(folder, type, filename)


def get_upload_path_course_thumbnails(instance, filename):
    # Use the sanitize_path_component function to sanitize the username
    safe_username = sanitize_path_component(instance.course.teacher.username)
    safe_course_name = sanitize_path_component(instance.course.name)

    folder = "users/"

    folder += f"{safe_username}/{safe_course_name}"  # Use sanitized username example: users/johndoe
    type = "thumbnails"
    # Call get_file_path with the sanitized folder, type, and filename example: users/johndoe/course/filename
    return get_file_path(folder, type, filename)
