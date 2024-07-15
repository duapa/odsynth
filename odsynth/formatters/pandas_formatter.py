from typing import Any, Dict, List

import pandas as pd

from .base_formatter import BaseFormatter
from .exceptions import DataWritePreparationException


class PandasDataframeFormatter(BaseFormatter):
    """Takes data generated in odsynth.DataGenerator and
    transforms it to a Pandas DataFrame."""

    def format_data(self, data: List[Dict[str, Any]]) -> pd.DataFrame:
        """Transforms data from odsynth.DataGenerator to a Pandas Dataframe.

        Parameters:
        -----------
        - data (list[dict]): Generated data from odsynth.DataGenerator

        Returns:
        --------
        output (pandas.DataFrame): Data transformed into a Pandas DataFrame.
        """
        return pd.DataFrame(data=data)

    @classmethod
    def get_name(cls) -> str:
        return "pandas"

    def prepare_for_writing(self, data: List[Dict[str, Any]]) -> List[str]:
        raise DataWritePreparationException(
            "Data preparation is not supported for PandasDataFrameFormatter"
        )

    @property
    def file_extension(self):
        raise DataWritePreparationException(
            "File write operations are not supported for PandasDataFrameFormatters"
        )
