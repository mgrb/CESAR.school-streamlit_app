"""Utility functions for loading files."""

from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st
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


@st.cache_data
def load_dataset(dataset_name: str) -> pd.DataFrame:
    """Loads a dataset from a csv file.

    Parameters
    ----------
    dataset_name : str
        Name of the dataset to be loaded.

    Returns
    -------
    pd.DataFrame
        Loaded dataset.

    """
    return pd.read_csv(
        Path(get_project_root()) / f'streamlit_app/data/{dataset_name}.csv',
    )


@st.cache_data
def load_ufs() -> list[str]:
    """Loads Brazilian states from a csv file.

    Returns
    -------
    list
        List of Brazilian states.

    """
    df_ufs = load_dataset('combustiveis-estados')

    estados = df_ufs['estado'].dropna().unique()
    estados.sort()

    return estados.tolist()


@st.cache_data
def load_meses_refeferencia() -> list[str]:
    """Loads Brazilian states from a csv file.

    Returns
    -------
    list
        List of Brazilian states.

    """
    df_ufs = load_dataset('combustiveis-estados')

    meses = df_ufs['referencia'].dropna().unique()
    meses.sort()

    return meses.tolist()
