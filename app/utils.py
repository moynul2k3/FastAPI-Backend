from applications.user.models import Permission
from tortoise import Tortoise

DEFAULT_ACTIONS = ["view", "add", "update", "delete"]

async def sync_permissions():
    apps = Tortoise.apps
    existing_models = []
    for app, models in apps.items():
        for model_name, model in models.items():
            if model.__module__.startswith("applications."):
                existing_models.append(model_name.lower())
                for action in DEFAULT_ACTIONS:
                    codename = f"{action}_{model_name.lower()}"
                    name = f"Can {action} {model_name}"
                    await Permission.get_or_create(codename=codename, defaults={"name": name})

    
    valid_codenames = [f"{action}_{m}" for m in existing_models for action in DEFAULT_ACTIONS]
    await Permission.exclude(codename__in=valid_codenames).delete()
    
    
import uuid
from slugify import slugify 

def generate_random_suffix(length=5):
    return uuid.uuid4().hex[:length]

async def generate_unique(
    text: str,
    model,
    field: str = "username",
    max_length: int = 50,
    suffix_length: int = 5,
):
    # Make sure base slug fits within max length (reserving space for suffix)
    base_slug = slugify(text)[: max_length - suffix_length]
    slug = f"{base_slug}{generate_random_suffix(suffix_length)}"

    # Keep regenerating until slug is unique
    while await model.filter(**{field: slug}).exists():
        slug = f"{base_slug}{generate_random_suffix(suffix_length)}"

    return slug