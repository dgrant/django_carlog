import os


def app_version(request):
    """Return app version and deployment info."""
    version = os.environ.get("APP_VERSION")
    is_docker = os.environ.get("DJANGO_SETTINGS_MODULE", "").endswith(".docker")

    if version:
        display = f"{version} (docker)" if is_docker else version
    else:
        display = "(docker)" if is_docker else ""

    return {"app_version": display}
