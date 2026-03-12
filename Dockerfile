
FROM python:3.12-slim
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt .
# Fix requirements.txt if it was saved as UTF-16 on Windows (remove null bytes)
RUN python -c "p='/code/requirements.txt'; b=open(p,'rb').read(); open(p,'wb').write(b.replace(b'\\x00', b''))"
RUN pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
