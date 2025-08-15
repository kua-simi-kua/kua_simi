FROM python:3

COPY alerts-requirements.txt .  
RUN python3 -m pip install --no-cache-dir -r alerts-requirements.txt
ENTRYPOINT ["./docker/alerts/entrypoint.sh"]