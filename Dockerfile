FROM python:3.12

RUN apt-get update && apt-get install -y
COPY requirement.txt ./app/requirement.txt
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirement.txt
CMD ["python", "-u", "main.py"]