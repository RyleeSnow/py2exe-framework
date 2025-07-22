from __future__ import annotations

import os
import warnings
from pathlib import Path

import pandas as pd
from my_logger import logger, setup_logger

warnings.filterwarnings('ignore')


def main_process(args_dict: dict) -> None:
    if 'logs_folder' in args_dict:
        setup_logger(args_dict['logs_folder'])

    examples_folder = str(Path(__file__).parents[2].joinpath('examples'))
    df = pd.read_csv(os.path.join(examples_folder, 'sample_data.csv'))
    logger.info(f"DataFrame loaded with {len(df)} rows and {len(df.columns)} columns.")

    print(df.head())
