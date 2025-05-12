FROM python:3.12-slim

RUN useradd -m -u 1000 appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 5001

ENV FLASK_APP=app
ENV FLASK_ENV=production

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:create_app()"]