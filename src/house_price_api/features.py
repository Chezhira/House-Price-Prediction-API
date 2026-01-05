import numpy as np
import pandas as pd

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Safe numeric conversions (if columns missing, they become NaN and are handled later)
    for c in ["Gr_Liv_Area", "Total_Bsmt_SF", "TotRms_AbvGrd", "Bedroom_AbvGr", "Full_Bath", "Half_Bath", "Year_Built", "Year_Remod_Add", "Year_Sold"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # Total living area proxy
    if "Gr_Liv_Area" in df.columns and "Total_Bsmt_SF" in df.columns:
        df["Total_Liv_Area"] = df["Gr_Liv_Area"].fillna(0) + df["Total_Bsmt_SF"].fillna(0)

    # Rooms ratio
    if "Gr_Liv_Area" in df.columns and "TotRms_AbvGrd" in df.columns:
        denom = df["TotRms_AbvGrd"].replace(0, np.nan)
        df["LivArea_per_Room"] = df["Gr_Liv_Area"] / denom

    # Basement ratio
    if "Total_Bsmt_SF" in df.columns and "Gr_Liv_Area" in df.columns:
        denom = df["Gr_Liv_Area"].replace(0, np.nan)
        df["Bsmt_Ratio"] = df["Total_Bsmt_SF"] / denom

    # Age / remodel features
    if "Year_Sold" in df.columns and "Year_Built" in df.columns:
        df["House_Age"] = df["Year_Sold"] - df["Year_Built"]
    if "Year_Remod_Add" in df.columns and "Year_Built" in df.columns:
        df["Remodeled"] = (df["Year_Remod_Add"] > df["Year_Built"]).astype("Int64")
    if "Year_Sold" in df.columns and "Year_Remod_Add" in df.columns:
        df["Years_Since_Remodel"] = df["Year_Sold"] - df["Year_Remod_Add"]

    # Log features
    if "Gr_Liv_Area" in df.columns:
        df["Log_Gr_Liv_Area"] = np.log1p(df["Gr_Liv_Area"].clip(lower=0))
    if "Total_Bsmt_SF" in df.columns:
        df["Log_Total_Bsmt_SF"] = np.log1p(df["Total_Bsmt_SF"].clip(lower=0))

    return df

def align_columns(df: pd.DataFrame, feature_columns: list[str]) -> pd.DataFrame:
    df = df.copy()
    # Add any missing columns as NaN
    for col in feature_columns:
        if col not in df.columns:
            df[col] = np.nan
    # Drop extras, keep training order
    return df[feature_columns]

def sanitize_cat_cols(X: pd.DataFrame, cat_cols: list[str]) -> pd.DataFrame:
    X = X.copy()
    for c in cat_cols:
        if c in X.columns:
            # CatBoost requires string/int for categorical; convert NaN to "__MISSING__"
            X[c] = X[c].astype("string").fillna("__MISSING__")
    return X

def sanitize_numeric_cols(X: pd.DataFrame, cat_cols: list[str]) -> pd.DataFrame:
    X = X.copy()
    num_cols = [c for c in X.columns if c not in set(cat_cols)]
    for c in num_cols:
        X[c] = pd.to_numeric(X[c], errors="coerce")
    return X
