FROM python:3.13

## Do not create PYC files - save disk space
ENV PYTHONDONTWRITEBYTECODE=1
## Do not use buffer for log - write immediately
ENV PYTHONUNBUFFERED=1
ENV FLASK_SECRET_KEY="Did-you-forget-about-me"

ADD requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /ProjectPlanner
ADD source/ .

RUN pytest

EXPOSE 8666

CMD ["python", "/ProjectPlanner/main.py"]