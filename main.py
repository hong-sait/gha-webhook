import os
import logging
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from deploy_cicd_demo import deploy_cicd_demo
from logger_config import get_logger


# Try to get WEBHOOK_SECRET (from env or .env file)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
if not WEBHOOK_SECRET:
    raise RuntimeError(
        "Environment variable WEBHOOK_SECRET is required but not set. Server will not start for security reasons."
    )


app = FastAPI(title="Docker Push Webhook Listener")


logger = get_logger(__name__)


# Optional: Allow CORS if needed (e.g., from frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Simple validation model (optional)
class WebhookPayload(BaseModel):
    repository: str
    tag: str
    pushed_by: str
    github_repo: str
    github_commit: str
    timestamp: str | None


@app.post("/webhook/docker-push")
def handle_docker_push(payload: WebhookPayload, x_token: str = Header(...)):
    """
    Secure webhook endpoint: rejects request if token is missing or invalid.
    """
    if x_token != WEBHOOK_SECRET:
        logger.warning("Unauthorized access attempt: Invalid or missing token")
        raise HTTPException(status_code=403, detail="Invalid or missing token")

    logger.info("🪝 Webhook received and authenticated.")
    logger.info(f"📦 Deploy {payload.repository}:{payload.tag} to K8s...")

    # Deploy cicd-demo-service
    try:
        yaml_path = os.path.join(os.path.dirname(__file__), "cicd-demo.yaml")
        deploy_cicd_demo(yaml_path)
        return {
            "status": "success",
            "message": "Docker image push event processed and deployment applied.",
        }
    except Exception as e:
        error_msg = f"Deployment failed: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error during deployment. Check logs for details.")


@app.get("/")
def read_root():
    return {"message": "Webhook server is running. Use POST /webhook/docker-push"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8642, reload=True)
