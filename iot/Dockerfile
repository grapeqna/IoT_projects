FROM python

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 3000

ENTRYPOINT python app.py