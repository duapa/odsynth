from typing import Any, Dict, List

import pandas as pd

from .abstract_transformer import AbstractTransformer


class PandasDataframeTransformer(AbstractTransformer):
    def transform(self, data: List[Dict[str, Any]]):
        return pd.DataFrame(data=data)
