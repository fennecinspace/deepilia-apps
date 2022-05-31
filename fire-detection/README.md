## Without docker : 

- Install requirements : 

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
docker build -t app-fire-detection:1.0 .
docker container run -p 8001:8001 -v $(pwd):/app app-fire-detection:1.0
```

- Option 3 : use a prebuilt image :

```
docker container run -p 8001:8001 -v $(pwd):/app fennecinspace/app-fire-detection:1.0
```


## Test request (local file upload with curl) :

```
curl -i -X POST -F image=@path/to/test/image.jpg http://127.0.0.1:8001/upload
```