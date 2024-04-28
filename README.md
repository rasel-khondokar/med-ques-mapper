# med-ques-mapper
## Installation and run commands for Mac OS
#### Install

```python3 -m venv venv```

```source venv/bin/activate```

```python3 -m pip install --upgrade pip```

```pip3 install -r requirements.txt```
#### run
```python __main__.py```
#### Result
*DATASET/output/out.json*

## Build and run commands for docker
```docker-compose up --build -d```

```docker cp <container_id>:/app/DATASET/output/out.json . ```
#### Result
*out.json*