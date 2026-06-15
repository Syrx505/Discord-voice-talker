FROM python:3.9-slim

# FFmpeg və libopus-dev quraşdırırıq (səs üçün vacibdir)
RUN apt-get update && apt-get install -y ffmpeg libopus-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Kitabxanaları quraşdırırıq
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
