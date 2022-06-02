## Without docker : 

- Clone YoloV5 and Install its requirements : 

```
git clone https://github.com/ultralytics/yolov5
pip install -r yolov5/requirements.txt
```

- Install server requirements:

```
pip install -r requirements.txt
```

- Run server

```
python server.py
```


## With docker : 

- Option 1 : use docker compose

```
docker-compose up
```

- Option 2 : build an image and launch a container :

```
docker build -t app-excavator-localization:1.0 .
docker container run -p 8001:8001 -v $(pwd):/app app-excavator-localization:1.0
```

- Option 3 : use a prebuilt image :

```
docker container run -p 8001:8001 -v $(pwd):/app fennecinspace/app-excavator-localization:1.0
```


## Test request (local file upload with curl) :

```
curl -i -X POST -F image=@path/to/test/image.jpg http://127.0.0.1:8001/upload
```