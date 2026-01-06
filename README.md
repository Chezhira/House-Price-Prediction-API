# 🏠 House Price Prediction API  
**CatBoost · FastAPI · Production-ready ML service**

## Overview
This project builds and deploys a **house price prediction service** using a gradient-boosted tree model trained on structured real-estate data.  
The focus is not only on model accuracy, but on **production readiness**: reproducibility, validation, testing, and API-based inference.

The final model is served via a **FastAPI** application with schema validation, versioned artifacts, and automated tests.

---

## Problem Statement
Accurately predict residential house prices based on property characteristics such as size, age, rooms, basement area, and sale timing, and expose predictions through a reliable HTTP API suitable for real-world integration.

---

## Modeling Approach
- **Algorithm**: CatBoost Regressor (gradient-boosted decision trees)
- **Why CatBoost**:
  - Strong performance on tabular data
  - Native handling of categorical features
  - Robust to feature scaling and missing values
- **Target**: Sale price (with experiments on log-transformed targets)

### Feature Engineering Highlights
- Total living area aggregation
- Ratios (e.g. basement vs living area)
- Property age and years since remodel
- Log transforms for highly skewed variables
- Explicit categorical feature handling

---

## Model Performance
Validation metrics (hold-out set):

| Metric | Value |
|------|------|
| MAE | **~12,800** |
| Median Absolute Error | ~8,100 |
| Mean Error (bias) | ~970 |
| 95th Percentile Absolute Error | ~37,700 |

These results indicate strong central accuracy with reasonable tail behavior, which was explicitly analyzed.

---

## Production Architecture
This repository follows a **clean, production-oriented layout**:
