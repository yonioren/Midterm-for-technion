FROM python:3.13

ENV PYTHONDONTWRITEBYTECODE=1 ## Do not create PYC files - save disk space
ENV PYTHONUNBUFFERED=1 ## Do not use buffer for log - write immediately

COPY ../Python/requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /ProjectPlanner
COPY ../Python/source .

EXPOSE 6666

CMD ["python", "/ProjectPlanner/main.py"]