FROM python:alpine AS build

WORKDIR /build_code
COPY ./training .
RUN pip install --no-cache-dir --upgrade -r requirements.txt && python3 main.py --preprocess


FROM python:alpine AS deploy

WORKDIR /deploy_code
COPY ./fastapi .
COPY --from=build /build_code/training_data/processed_data/model.pkl /deploy_code/model.pkl

ENTRYPOINT [ "python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0" ]

EXPOSE 8000
