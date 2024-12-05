from rest_framework.exceptions import ErrorDetail
from rest_framework import status
from rest_framework.response import Response
from urllib.parse import quote
import os
from rest_framework.views import exception_handler


def get_file_path(folder, type, filename):
    # Create the folder path with the name
    folder_path = f"{folder}/{type}/"
    # Return the full file path
    print("folder_path", folder_path)
    return os.path.join(folder_path, filename)


def sanitize_path_component(path_component):
    safe_component = quote(path_component, safe="")
    return "".join(
        [c if c.isalnum() or c in (" ", "-", "_") else "_" for c in safe_component]
    )


def flatten_errors(errors):
    flattened_errors = []

    # Check if errors is a list of ErrorDetail objects or a single string
    if isinstance(errors, list) and all(
        isinstance(error, ErrorDetail) for error in errors
    ):
        return " ".join(str(error) for error in errors)
    elif isinstance(errors, str):  # Directly return the string if errors is a string
        return errors

    non_field_errors = errors.pop("non_field_errors", None)
    for field, messages in errors.items():
        if isinstance(messages, dict):  # Check if the error is nested
            errors = {**errors, **messages}
            errors.pop(field)
            for key, value in messages.items():
                # Ensure messages are treated as lists before joining
                if isinstance(value, list):
                    flattened_errors.append(" ".join(str(message) for message in value))
                else:
                    flattened_errors.append(str(value))
        else:
            # Ensure messages are treated as lists before joining
            if isinstance(messages, list):
                flattened_errors.append(" ".join(str(message) for message in messages))
            else:
                flattened_errors.append(str(messages))
    if non_field_errors is not None:
        # Ensure non_field_errors are treated as lists before extending
        if isinstance(non_field_errors, list):
            flattened_errors.extend(non_field_errors)
        else:
            flattened_errors.append(str(non_field_errors))
    return " ".join(flattened_errors)


def handle_validation_error(e):
    errors = e.detail
    print("errors here", errors)
    flattened_errors = flatten_errors(errors)
    print("here flattened_errors", flattened_errors)
    return Response({"error": flattened_errors}, status=status.HTTP_400_BAD_REQUEST)


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data["status_code"] = response.status_code

    return response
