FROM python:3

COPY stats-requirements.txt .  
RUN python3 -m pip install --no-cache-dir -r stats-requirements.txt
ENTRYPOINT ["./docker/stats/entrypoint.sh"]