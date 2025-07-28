FROM python as first

WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt -t /app

COPY app.py .

FROM alpine as second

WORKDIR /app

RUN apk add python3

COPY --from=first /app /app
COPY --from=first /app/app.py /app

CMD [ "python3", "app.py" ]