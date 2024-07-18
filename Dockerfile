FROM python:3

# RUN python3 -m pip install --no-cache-dir -r requirements.txt
# VOLUME [$GITHUB_WORKSPACE]
CMD ["ls", "-al", "/github/workspace"]
