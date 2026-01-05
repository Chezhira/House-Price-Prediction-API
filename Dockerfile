FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md /app/
COPY src /app/src
COPY artifacts /app/artifacts

RUN pip install --no-cache-dir -e .

ENV HOST=0.0.0.0
ENV PORT=8000
ENV MODEL_VERSION=v1
EXPOSE 8000

CMD ["uvicorn", "house_price_api.app:app", "--host", "0.0.0.0", "--port", "8000"]
