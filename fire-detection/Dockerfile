FROM python:3.8-slim
WORKDIR /app
ADD . /app
RUN apt-get update && apt-get install -y --no-install-recommends libgl1 libglib2.0-0
RUN pip install -r requirements.txt
EXPOSE 8001
CMD ["python3", "server.py"]