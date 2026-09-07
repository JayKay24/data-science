FROM python:3.11-slim

WORKDIR /app
COPY projects/churn_prediction/churn_service.pex /app/churn_service.pex

EXPOSE 8000
ENTRYPOINT ["/usr/local/bin/python", "/app/churn_service.pex"]
