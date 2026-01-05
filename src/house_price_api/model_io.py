import json
from pathlib import Path
from functools import lru_cache
from catboost import CatBoostRegressor

from .config import settings

def _artifact_paths():
    root = Path(settings.artifacts_dir) / settings.model_version
    return {
        "root": root,
        "model": root / "catboost_house_price.cbm",
        "feature_columns": root / "feature_columns.json",
        "cat_cols": root / "cat_cols.json",
    }

@lru_cache(maxsize=1)
def load_artifacts():
    paths = _artifact_paths()
    root = paths["root"]

    if not root.exists():
        raise FileNotFoundError(f"Artifacts folder not found: {root.resolve()}")

    model_path = paths["model"]
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path.resolve()}")

    model = CatBoostRegressor()
    model.load_model(str(model_path))

    feature_columns = json.loads(paths["feature_columns"].read_text(encoding="utf-8"))
    cat_cols = json.loads(paths["cat_cols"].read_text(encoding="utf-8"))

    return model, feature_columns, cat_cols
