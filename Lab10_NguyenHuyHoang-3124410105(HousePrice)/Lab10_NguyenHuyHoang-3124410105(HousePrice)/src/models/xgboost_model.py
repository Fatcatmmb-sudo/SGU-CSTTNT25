from xgboost import XGBRegressor
from src.models.base_model import BaseModel


class XGBoostModel(BaseModel):
    def __init__(self, **params):
        super().__init__(name="XGBoost")
        self.build_model(params)

    def build_model(self, params):
        self.model = XGBRegressor(**params)
