from fastapi.testclient import TestClient
from house_price_api.app import app

client = TestClient(app)

def test_predict_minimal_fields():
    payload = {
        "record": {
            "Gr_Liv_Area": 1710,
            "TotRms_AbvGrd": 8,
            "Total_Bsmt_SF": 856,
            "Year_Built": 2003,
            "Year_Remod_Add": 2003,
            "Year_Sold": 2010
        }
    }
    r = client.post("/predict", json=payload)
    assert r.status_code == 200, r.text
    body = r.json()
    assert isinstance(body["prediction"], float)
