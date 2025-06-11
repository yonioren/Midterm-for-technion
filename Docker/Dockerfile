FROM python:3.13

ENV PYTHONDONTWRITEBYTECODE=1 ## Do not create PYC files - save disk space
ENV PYTHONUNBUFFERED=1 ## Do not use buffer for log - write immediately

WORKDIR /Midterm

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY python .

EXPOSE 8080

CMD ["python", "main.py"]
