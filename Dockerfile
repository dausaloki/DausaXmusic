FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ffmpeg git build-essential libssl-dev libffi-dev \
      libopus0 libopus-dev libgl1 libglib2.0-0 libsm6 libxext6 libxrender1 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt && \
    python -c "import yt_dlp, yt_dlp_ejs" && \
    deno --version && \
    ffmpeg -version > /dev/null

COPY . .
CMD ["python", "-m", "DAUSAXMUSIC"]
