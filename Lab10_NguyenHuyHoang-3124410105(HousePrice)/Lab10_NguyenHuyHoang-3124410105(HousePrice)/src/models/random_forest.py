from sklearn.ensemble import RandomForestRegressor
from src.models.base_model import BaseModel


class RandomForestModel(BaseModel):
    def __init__(self, **params):
        super().__init__(name="RandomForest")
        self.build_model(params)

    def build_model(self, params):
        self.model = RandomForestRegressor(**params)
