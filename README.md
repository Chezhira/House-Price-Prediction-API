# House Price API (CatBoost + FastAPI)

Artifacts are versioned under `artifacts/v1/`.

## Run locally (Conda)
```powershell
conda activate ml311
cd C:\Users\ziddm\data-work\house-price-api
pip install -e .
pytest -q
uvicorn house_price_api.app:app --reload --host 127.0.0.1 --port 8000
```

Swagger:
- http://127.0.0.1:8000/docs

## Example request (PowerShell)
```powershell
irm "http://127.0.0.1:8000/predict" -Method Post -ContentType "application/json" -Body '{"record":{"Gr_Liv_Area":1710,"TotRms_AbvGrd":8,"Total_Bsmt_SF":856,"Year_Built":2003,"Year_Remod_Add":2003,"Year_Sold":2010}}'
```
