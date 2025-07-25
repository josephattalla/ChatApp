FROM python:3

WORKDIR /app

EXPOSE 8000

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

WORKDIR /

CMD ["sh", "-c", "python -m app.db_functions && fastapi run /app/main.py --port 8000"]
