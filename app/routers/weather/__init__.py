from fastapi import APIRouter, Request
import requests
import os
import dotenv; dotenv.load_dotenv()
import datetime
import pandas as pd
import time
import asyncio

router = APIRouter(prefix="/weather")

@router.post("/save_api_token")
async def save_api_token(request: Request):
    data = await request.json()
    api_token = data.get('api_token')

    if not api_token:
        return {
            'error': 'No API token provided'
        }
    
    df = pd.DataFrame({'api_token': [api_token]})
    df.to_csv('app/data/api_token.csv', index=False)

    return {
        'status': 'API token saved'
    }


@router.post("/request_data")
async def request_data(request: Request):
    data = await request.json()

    request_id = str(data.get('request_id'))
    cities = data.get('cities')

    request_status = pd.read_csv('app/data/request_status.csv')

    if str(request_id) in request_status['request_id'].astype(str).unique():
        return {
            'request_id': request_id,
            'error': 'Request ID already exists',
            'msg': 'Use a different request ID'
        }

    if not cities:
        return {
            'request_id': request_id,
            'error': 'No cities provided'
        }

    if not isinstance(cities, list):
        cities = [cities]
    
    asyncio.create_task(save_data(request_id, cities, request_status))

    return {
        'request_id': request_id,
        'status': 'Data request received'
    }

@router.get("/check_progress")
async def check_progress(request: Request):
    data = await request.json()

    request_id = data.get('request_id')

    request_status = pd.read_csv('app/data/request_status.csv')
    data = request_status[request_status['request_id'].astype(str) == str(request_id)]

    if data.empty:
        return {
            'request_id': request_id,
            'error': 'Request ID not found'
        }

    return data.to_dict(orient='records')

@router.post("/see_results")
async def see_results(request: Request):
    data = await request.json()
    request_id = data.get('request_id')

    data = pd.read_csv('app/data/data.csv')
    data = data[data['request_id'].astype(str) == str(request_id)]

    if data.empty:
        return {
            'request_id': request_id,
            'error': 'Request ID not found'
        }

    return data.to_dict(orient='records')

async def save_data(request_id, cities, request_status):
    result = []

    for i, j in enumerate(cities):
        print(j)
        print(get_data(j))
        result.append(get_data(j))
        data = {'request_id': [str(request_id)], 'complete_pct': [(i + 1) / len(cities) * 100]}
        
        request_status = pd.concat([request_status, pd.DataFrame(data)], ignore_index=True)
        request_status.drop_duplicates(subset=['request_id'], keep='last', inplace=True)

        request_status.to_csv('app/data/request_status.csv', index=False)

        data = pd.read_csv('app/data/data.csv')

        df = {'request_id': request_id, 'data': result}
        df = pd.DataFrame(df)

        data = pd.concat([data, df], ignore_index=True)

        data.to_csv('app/data/data.csv', index=False)
        
        time.sleep(1)

    return

def get_data(id):
    api_token = pd.read_csv('app/data/api_token.csv')

    if api_token.empty:
        return {
            'error': 'No API token',
            'msg': 'README.md teaches you how to save the token'
        }
    
    API_TOKEN = api_token['api_token'].values[0]

    url = f'https://api.openweathermap.org/data/2.5/weather?id={id}&appid={API_TOKEN}'
    data = {'units': 'metric'}

    req = requests.get(url, params=data)

    if req.status_code >= 300:
        print(req.status_code)
        return {
            'id': 'id',
            'error': 'City not found'
        }

    data = {
        'city_id': id,
        'temp': req.json().get('main').get('temp'),
        'humidity': req.json().get('main').get('humidity'),
        'request_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    return data