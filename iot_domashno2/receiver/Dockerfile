FROM python as first 
# ve4e nqma vtoro

WORKDIR /app
COPY . .

EXPOSE 3000
VOLUME [ "/static" ]

RUN ["pip", "install", "-r", "requirements.txt"]

CMD [ "python3", "app.py" ]
