conda activate ml311
cd $PSScriptRoot
$env:MODEL_VERSION="v1"
uvicorn house_price_api.app:app --reload --host 127.0.0.1 --port 8000
