# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python webhook listener for GitHub Actions that automatically deploys OCI images to a Kubernetes cluster when notified. The system consists of:
- A FastAPI webhook server that receives GitHub Actions notifications
- A deployment script that manages Kubernetes resources via kubectl
- A YAML manifest for the Kubernetes deployment and service

## Key Components

1. **main.py**: FastAPI server with a secure webhook endpoint at `/webhook/docker-push`
2. **deploy_cicd_demo.py**: Kubernetes deployment management script
3. **cicd-demo.yaml**: Kubernetes deployment and service manifest
4. **logger_config.py**: Centralized logging configuration

## Development Setup

To set up the development environment:
1. Ensure Python 3.13+ is installed
2. Install dependencies with `pip install .` or `pip install -e .` for development
3. Create a `.env` file with `WEBHOOK_SECRET=your_secret_here`

## Common Commands

- **Run server**: `python main.py` or `uvicorn main:app --host 0.0.0.0 --port 8642 --reload`
- **Lint**: `ruff check .` or `ruff .`
- **Format**: `ruff format .` (if configured)
- **Deploy manually**: `python deploy_cicd_demo.py`

## Architecture Notes

- The webhook requires a valid `X-Token` header matching the `WEBHOOK_SECRET` environment variable
- The deployment process deletes the existing deployment before applying the new one to ensure a clean state
- Security context is configured in the Kubernetes YAML with non-root user, dropped capabilities, and seccomp profile
- Logging uses a centralized configuration with consistent formatting
- The server uses CORS middleware (currently permissive for development)

## Security Considerations

- WEBHOOK_SECRET must be set in environment variables or .env file
- All webhook requests must include a valid X-Token header
- Kubernetes operations are performed via subprocess calls to kubectl
- SecurityContext in the deployment YAML enforces security best practices