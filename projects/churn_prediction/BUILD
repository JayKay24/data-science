python_sources(
    name="sources",
    sources=["churn_prediction/**/*.py"],
    resolve="churn_resolve",
    dependencies=[
        "libs/core:core_lib@resolve=churn_resolve",
    ],
)

python_tests(
    name="tests",
    sources=["churn_prediction/**/test_*.py"],
    resolve="churn_resolve",
    dependencies=[
        ":sources",
    ],
)

pex_binary(
    name="train_bin",
    entry_point="churn_prediction.train:train_model",
    resolve="churn_resolve",
    dependencies=[
        ":sources",
    ],
)

pex_binary(
    name="churn_service",
    entry_point="uvicorn.main:main",
    args=["churn_prediction.app:app", "--host", "0.0.0.0", "--port", "8000"],
    resolve="churn_resolve",
    dependencies=[
        ":sources",
    ],
)

docker_image(
    name="docker",
    dependencies=[":churn_service"],
    instructions=[
        "FROM python:3.11-slim",
        "WORKDIR /app",
        "COPY projects.churn_prediction/churn_service.pex /app/churn_service.pex",
        "EXPOSE 8000",
        'ENTRYPOINT ["/usr/local/bin/python", "/app/churn_service.pex"]',
    ],
)
