run:
	uvicorn house_price_api.app:app --reload --host 127.0.0.1 --port 8000

test:
	pytest -q

docker-build:
	docker build -t house-price-api:latest .

docker-run:
	docker run -p 8000:8000 house-price-api:latest
