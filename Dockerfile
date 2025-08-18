FROM python:3.12-slim

WORKDIR /app

# deps first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# your code
COPY . ./

# tiny launcher that starts both, then waits
RUN printf '%s\n' \
'#!/usr/bin/env bash' \
'python -m uvicorn app_api:app --host 0.0.0.0 --port 8010 &' \
'wait -n' \
> /start.sh && chmod +x /start.sh

EXPOSE 8010
CMD ["/bin/bash", "/start.sh"]
