FROM python:3.12.7-bullseye


WORKDIR /app
COPY requirements.txt .

RUN python -m venv .venv
ENV PATH="/.venv/bin:$PATH"

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .




CMD ["python", "bot"]