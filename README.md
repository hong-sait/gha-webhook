# gha-webhook

A simple webhook listener for GitHub Actions.

This server listens for webhook notifications from GitHub Actions workflow, and upon receiving a valid notification, it will deploy the OCI image to K8s cluster.

Locking requirements
```
uv pip compile pyproject.toml -o requirements.txt
```
