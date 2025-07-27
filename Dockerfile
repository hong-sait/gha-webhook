# Use Python 3.13 base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install curl for downloading kubectl and uv
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Download and install kubectl (latest stable version for Linux x86_64)
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
  install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl && \
  rm kubectl

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="/usr/bin/" sh

# Copy project files
COPY . .

# Install Python dependencies with uv
RUN uv venv --clear && uv sync

# Expose port
EXPOSE 8642

# Run the application with uv
ENTRYPOINT ["uv", "run", "main.py"]
