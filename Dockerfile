FROM python:3.9-slim

# FFmpeg və libopus quraşdırırıq (səsin kəsilməməsi üçün)
RUN apt-get update && apt-get install -y ffmpeg libopus-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Kitabxanaları quraşdırırıq
RUN pip install --no-cache-dir -r requirements.txt

# Botu işə salırıq
CMD ["python", "main.py"]
