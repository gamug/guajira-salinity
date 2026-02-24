import os
import config

import pandas as pd
from ydata_profiling import ProfileReport

def check_directories():
    """Ensure that all configured directories exist on the filesystem.

    This function iterates over the directory paths defined in the configuration
    and creates any that do not already exist.

    Args:
        None

    Returns:
        None
    """
    for dir in config.path.values():
        os.makedirs(dir, exist_ok=True)
        
def profile_dataset(dataset: pd.DataFrame, name: str='name_not_defined', save: bool=False) -> None:
    """Generate a profiling report for a given dataset.
    This function uses the ydata_profiling library to create a comprehensive report
    of the dataset's characteristics, including data types, missing values, and
    statistical summaries.
    Args:
        dataset (pd.DataFrame): The dataset to be profiled.
        name (str): A name for the dataset, used in the report title and filename.
        save (bool): Whether to save the report as an HTML file in the data engineering directory.
    Returns:
        ProfileReport: The generated profiling report object.
    """
    profile = ProfileReport(dataset, title=name)
    if save:
        # save the report as an HTML file
        profile.to_file(os.path.join(config.path['data_engineering'], f'{name}.html'))
    return profile