FROM python:3

COPY statsnalerts-requirements.txt .  
RUN python3 -m pip install --no-cache-dir -r stats-requirements.txt
ENTRYPOINT ["./docker/alerts/entrypoint.sh"]