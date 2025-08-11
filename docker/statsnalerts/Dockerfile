FROM python:3

COPY statsnalerts-requirements.txt .  
RUN python3 -m pip install --no-cache-dir -r statsnalerts-requirements.txt
# CMD python3 ./scripts/auth_repo_metadata_pull.py ./config/repos_list_1.json
# COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["./docker/statsnalerts/entrypoint.sh"]