## devgrid-test

Steps to use API

1. Starts docker container. On CMD, navigate to the project folder and run the following command:
```bash
docker build -t myimage .
```
```bash
docker run -d --name mycontainer -p 8000:8000 myimage
```

2. Send your API Token to this URL:
```python
url = 'http://localhost:8000/weather/request_data'
data = json.dumps({'api_token': your_api_token})

requests.post(url, data=data)
```

3. POST route to request data from an Open Weather API:
(example)

```python
url = 'http://localhost:8000/weather/request_data'
data = json.dumps({'request_id': '1234', 'cities': [3439525, 3439781, 3440645,]})

req = requests.post(url, data=data)
```

4. GET route to check progress with the percentage of the
POST progress ID (collected cities completed) until the current moment.:

```python
url = 'http://localhost:8000/weather/check_progress'
data = json.dumps({'request_id': '12345'})

req = requests.get(url, data=data)
print(req.json())
```

5. Route to receive data from the requested cities:

```python
url = 'http://localhost:8000/weather/see_results'
data = json.dumps({'request_id': '12345'})

req = requests.post(url, data=data)
print(req.json())
```
