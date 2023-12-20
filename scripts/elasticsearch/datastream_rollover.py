from elasticsearch import Elasticsearch
from dotenv import load_dotenv

import requests, os

def get_data_streams(es_client):
    return es_client.indices.get_data_stream()["data_streams"] 

def rollover_data_stream(data_stream_name, es_url, es_user, es_password):
    # pass in basic auth credentials

    url = f"{es_url}/{data_stream_name}/_rollover"
    
    auth = (es_user, es_password)
    response = requests.post(
        url=url,
        auth=auth,
    )
    
    return response.json() if response.ok else f"Failed with status code: {response.status_code}"

if __name__ == '__main__':
    load_dotenv('.env')
    es_url = os.environ['ES_URL']
    es_password = os.environ['ES_PASSWORD']
    es_user = os.environ['ES_USER']
    datastream_prefix = "xyz"

    # Initialize Elasticsearch client
    es = Elasticsearch(
        es_url, basic_auth=(es_user, es_password)
    )

    # Get a list of data streams
    data_streams = get_data_streams(es)

    # Perform rollover for each data stream
    for stream in data_streams:
        data_stream_name = stream['name']
        # only rollover data stream name if it contains "datastream_prefix"
        if data_stream_name.startswith(datastream_prefix):
            rollover_response = rollover_data_stream(data_stream_name, es_url, es_user, es_password)
            print(f"Rollover executed for data stream: {data_stream_name}")
            print(rollover_response)
