FROM python:3.9
WORKDIR /Project/fine

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["index.py"]