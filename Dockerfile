# Use the official Python image as the base image
FROM python:3.11.5-slim

# Set the working directory to /app
WORKDIR /app

# Expose port 8080
EXPOSE 8080

# Copy the local files to the container at /app
COPY . .

# Install system dependencies and clean up
RUN apt-get update && \
    apt-get install -y \
        fonts-liberation \
        libasound2 \
        libatk-bridge2.0-0 \
        libatk1.0-0 \
        libatspi2.0-0 \
        libcups2 \
        libdbus-1-3 \
        libdrm2 \
        libgbm1 \
        libgtk-3-0 \
        libnspr4 \
        libnss3 \
        libx11-xcb1 \
        libxcb-dri3-0 \
        libxcomposite1 \
        libxdamage1 \
        libxfixes3 \
        libxrandr2 \
        xdg-utils \
        libgdk-pixbuf2.0-0 \
        wget && \
    dpkg -i ./drivers/google_chrome_86_0_4240_75.deb && \
    chmod a+x ./drivers/chromedriver && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt && \
    python -c 'import nltk; nltk.download("punkt")'

# Command to run on container start
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8080",  "src.fast_api:app"]