FROM python:3.12-slim

# Install dependencies
RUN pip install -U pdm
RUN apt-get update && apt-get install -y rclone

# Set working directory
WORKDIR /app

# Install dependencies
COPY pyproject.toml pdm.lock ./
RUN pdm install

# Copy source code
COPY src ./src

# Copy rclone.conf and config.yaml
COPY rclone.conf ./
COPY config.yaml ./

# Run the application
CMD ["pdm", "run", "python", "src/backblaze-runner/__main__.py"]
