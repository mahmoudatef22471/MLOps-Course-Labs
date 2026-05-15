# MLOps Course Labs

Welcome to the lab repository for the [MLOps Course](https://github.com/Heba-Atef99/MLOps-Course).

Throughout this hands-on journey, you'll develop a **Bank Customer Churn Prediction** application—starting from the research phase and progressing through the full MLOps lifecycle, all the way to deployment.

## Churn Prediction API

A Litestar API serving the churn prediction model with logging and tests.

### Setup

```bash
uv sync
uv run pre-commit install
# place your model in data/model.joblib
uv run litestar --app main:app run --reload
```

Swagger UI: http://localhost:8000/schema/swagger

### Tests

```bash
uv run pytest tests/ -v --cov=app --cov=main --cov-report=term-missing
```

### CI / CD and Deployment

This repository includes a GitHub Actions workflow at `.github/workflows/actions.yml`.

The workflow performs:
- dependency installation
- linting with `ruff`
- pre-commit validation
- pytest execution
- Docker image build
- image push to Docker Hub or AWS ECR, depending on secrets
- deployment to an EC2 instance via SSH

To use the workflow, add the following repository secrets in GitHub:
- `REGISTRY_PROVIDER` = `docker_hub` or `aws_ecr`
- `DOCKERHUB_USERNAME` and `DOCKERHUB_PASSWORD` (for Docker Hub)
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, `ECR_REGISTRY`, `ECR_REPOSITORY` (for AWS ECR)
- `EC2_HOST`, `EC2_USER`, `EC2_SSH_KEY`, and optionally `EC2_SSH_PORT`

### Endpoints

| Method | Path       | Description              |
| ------ | ---------- | ------------------------ |
| GET    | `/`        | Welcome message          |
| GET    | `/health`  | Health check             |
| POST   | `/predict` | Returns churn prediction |
