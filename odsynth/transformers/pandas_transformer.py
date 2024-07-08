from typing import Any, Dict, List

import pandas as pd

from .abstract_transformer import AbstractTransformer


class PandasDataframeTransformer(AbstractTransformer):
    """Takes data generated in odsynth.DataGenerator and
    transforms it to a Pandas DataFrame."""

    def transform(self, data: List[Dict[str, Any]]) -> pd.DataFrame:
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
