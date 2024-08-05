"""Utility functions for loading files."""

from pathlib import Path
from typing import Any

import toml
from PIL import Image


def get_project_root() -> str:
    """Returns project root path.

    Returns
    -------
    str
        Project root path.

    """
    return str(Path(__file__).parent.parent.parent)


def load_image(image_name: str) -> Image:
    """Displays an image.

    Parameters
    ----------
    image_name : str
        Local path of the image.

    Returns
    -------
    Image
        Image to be displayed.

    """
    return Image.open(
        Path(get_project_root()) / f'streamlit_app/assets/imgs/{image_name}',
    )


def load_toml(toml_file: str) -> dict[Any, Any]:
    """Loads config toml file from user's file system as a dictionary.

    Parameters
    ----------
    toml_file : str
        Uploaded toml config file.

    Returns
    -------
    dict
        Loaded config dictionary.

    """
    toml_loaded = toml.load(
        Path(get_project_root())
        / f'streamlit_app/assets/lang/{toml_file}.toml',
    )

    return dict(toml_loaded)
