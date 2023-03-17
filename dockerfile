FROM python:3.9

WORKDIR .

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=main.py

EXPOSE 8080

CMD ["flask", "run"]