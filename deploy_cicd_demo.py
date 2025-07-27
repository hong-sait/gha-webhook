import os
import subprocess
import time
from logger_config import get_logger


logger = get_logger(__name__)


def run_command(cmd, log_output=True):
    """
    Run a shell command and log stdout/stderr.
    :param cmd: Command to run (string)
    :param log_output: Whether to log output
    :return: subprocess.CompletedProcess
    """
    logger.info(f"Running command: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.stdout and log_output:
        for line in result.stdout.strip().splitlines():
            logger.info(f"stdout | {line}")
    if result.stderr and log_output:
        for line in result.stderr.strip().splitlines():
            if "not found" in line or "No resources found" in line:
                logger.info(f"stderr | {line}")  # Often informational
            else:
                logger.error(f"stderr | {line}")

    return result


def delete_deployment():
    """Delete the deployment and return True if successful or not found."""
    cmd = "kubectl delete deployment cicd-demo-deployment -n self-hosted"
    result = run_command(cmd, log_output=True)
    # Return True if deleted or already not found
    return result.returncode == 0 or "not found" in result.stderr.lower()


def check_deployment():
    """Check if the deployment exists."""
    cmd = "kubectl get deployment cicd-demo-deployment -n self-hosted"
    result = run_command(cmd, log_output=False)
    return result.returncode == 0  # True if deployment exists


def deploy_cicd_demo(yaml_path):
    """
    Deploy the CICD demo by deleting the old deployment and applying the YAML.
    Waits until the deployment is fully deleted before applying.

    :param yaml_path: Absolute path to cicd-demo.yaml
    """
    if not os.path.isfile(yaml_path):
        raise FileNotFoundError(f"YAML file not found at {yaml_path}")

    logger.info(f"Deleting resources defined in {yaml_path}...")
    delete_cmd = f"kubectl delete -f {yaml_path}"
    result = run_command(delete_cmd)

    if result.returncode != 0:
        msg = f"Failed to delete resources from {yaml_path}"
        logger.error(msg)
        raise RuntimeError(f"{msg}:\n{result.stderr}")

    logger.info("Waiting 3 seconds for deletion to propagate...")
    time.sleep(3)

    # Initial attempt to delete deployment
    delete_deployment()

    # Wait until deployment is fully gone
    while check_deployment():
        logger.info("Deployment still exists, waiting 3 seconds before retrying deletion...")
        time.sleep(3)
        delete_deployment()

    logger.info("Deployment deleted successfully, proceeding with apply")
    apply_cmd = f"kubectl apply -f {yaml_path}"
    result = run_command(apply_cmd)

    if result.returncode != 0:
        msg = f"Failed to apply the deployment from {yaml_path}"
        logger.error(msg)
        raise RuntimeError(f"{msg}:\n{result.stderr}")
    else:
        logger.info("Deployment applied successfully.")
        if result.stdout.strip():
            for line in result.stdout.strip().splitlines():
                logger.info(f"apply success | {line}")


def main():
    # Set WORK_DIR to the directory of this script
    work_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_file = os.path.join(work_dir, "cicd-demo.yaml")

    try:
        deploy_cicd_demo(yaml_file)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)


if __name__ == "__main__":
    import sys

    main()
