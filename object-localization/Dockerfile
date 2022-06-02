FROM python:3.8-slim
WORKDIR /app
ADD . /app
RUN apt-get update && apt-get install -y --no-install-recommends libgl1 libglib2.0-0 git
RUN rm -rf yolov5 && git clone https://github.com/ultralytics/yolov5
RUN pip install -r yolov5/requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8001
CMD ["python3", "server.py"]