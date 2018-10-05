"""handlers/datasets.py

Handle /datasets API endpoint.
"""

from typing import Mapping, List  # noqa: F401
from collections import OrderedDict

from terracotta import get_settings, get_driver
from terracotta.profile import trace


@trace('datasets_handler')
def datasets(some_keys: Mapping[str, str] = None) -> 'List[OrderedDict[str, str]]':
    """List all available key combinations"""
    settings = get_settings()
    driver = get_driver(settings.DRIVER_PATH, provider=settings.DRIVER_PROVIDER)

    with driver.connect():
        dataset_keys = driver.get_datasets(where=some_keys).keys()
        key_names = driver.key_names

    return [OrderedDict(zip(key_names, ds_keys)) for ds_keys in dataset_keys]
