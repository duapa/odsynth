from typing import Any, Dict, List

import pandas as pd

from .base_transformer import BaseTransformer


class PandasDataframeTransformer(BaseTransformer):
    def transform(self, data: List[Dict[str, Any]]):
        return pd.DataFrame(data=data)
