import docker
import tempfile
import os
import logging

logger = logging.getLogger(__name__)

class DockerSandbox:
    def __init__(self, image: str = "python:3.10-slim"):
        self.image = image
        try:
            # Connect to the local Docker daemon
            self.client = docker.from_env()
            # Verify we have the base image, otherwise pull it
            self.client.images.get(self.image)
        except docker.errors.ImageNotFound:
            logger.info(f"Pulling Docker image {self.image}... This might take a minute.")
            self.client.images.pull(self.image)
        except docker.errors.DockerException as e:
            logger.error("Failed to connect to Docker. Ensure Docker Desktop is running.")
            raise RuntimeError("Docker daemon not found.") from e

    def run_test(self, test_code: str) -> dict:
        """
        Executes the AI-generated pytest script in an isolated Docker container.
        Returns the execution logs and whether the test successfully crashed (reproduced the bug).
        """
        # 1. Create a temporary, ephemeral directory on the host machine
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file_path = os.path.join(temp_dir, "test_reproduction.py")
            
            # Write the AI's code to this temporary file
            with open(test_file_path, "w", encoding="utf-8") as f:
                f.write(test_code)
                
            try:
                # 2. Spin up the container, mount the temp file, and execute PyTest
                container_logs = self.client.containers.run(
                    image=self.image,
                    command='sh -c "pip install pytest -q && pytest /app/test_reproduction.py"',
                    volumes={temp_dir: {'bind': '/app', 'mode': 'ro'}}, # Read-only mount for security
                    working_dir="/app",
                    remove=True, # Auto-destroy the container immediately after execution
                    detach=False,
                    stdout=True,
                    stderr=True
                )
                
                # If it exits with 0 (no errors), it means the test passed. 
                # For a bug reproducer, a passing test means we FAILED to reproduce the crash!
                return {
                    "success": False, 
                    "exit_code": 0,
                    "logs": container_logs.decode("utf-8"),
                    "message": "The test ran successfully, meaning it failed to reproduce the bug."
                }
                
            except docker.errors.ContainerError as e:
                # ContainerError triggers when the script crashes (non-zero exit code).
                # In our case, a crash means the AI SUCCESSFULLY reproduced the bug!
                return {
                    "success": True, 
                    "exit_code": e.exit_status,
                    "logs": e.stderr.decode("utf-8") if e.stderr else e.stdout.decode("utf-8"),
                    "message": "Bug successfully reproduced in sandbox environment!"
                }
            except Exception as e:
                return {
                    "success": False,
                    "exit_code": -1,
                    "logs": str(e),
                    "message": "System error during sandbox execution."
                }