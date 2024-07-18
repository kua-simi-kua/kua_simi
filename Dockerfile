FROM python:3

COPY requirements.txt .  
RUN python3 -m pip install --no-cache-dir -r requirements.txt
# VOLUME [$GITHUB_WORKSPACE]
CMD ["ls", "-al"]
