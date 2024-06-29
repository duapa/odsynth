from typing import Any, Dict, List
from .base_transformer import BaseTransformer
import pandas as pd


class PandasDataframeTransformer(BaseTransformer):
    def transform(self, data: List[Dict[str, Any]]):
        return pd.DataFrame(data=data)