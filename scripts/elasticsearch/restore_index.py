from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionTimeout, ApiError
from dotenv import load_dotenv
import os
import time

# Maximum number of retry attempts
max_retries = 3

# Delay between retries (in seconds)
retry_delay = 1

def close_index(index_name):
    print(index_name)
    # Close the index
    # Retry loop
    for attempt in range(max_retries):
        try:
            response = es_client.indices.close(index=index_name)
        except ConnectionTimeout:
            print(f"Attempt {attempt+1} failed due to timeout. Retrying after {retry_delay} seconds...")
            time.sleep(retry_delay)  # Wait before retrying

    # Check the response to ensure the index was closed successfully
    if response['acknowledged']:
        print(f"Index '{index_name}' has been closed.")
    else:
        print(f"Failed to close index '{index_name}'.")

def restore_index(index_name, snapshot_name, repository_name):
    try:
        response = es_client.snapshot.restore(indices=index_name, include_aliases=True, snapshot=snapshot_name, repository=repository_name)
        # Check the response and handle success
        if response.get('accepted'):
            print(f"Snapshot '{snapshot_name}' has been restored to index '{index_name}'.")
        else:
            print("Snapshot restore was not accepted.")
    except ApiError  as e:
        error_message = str(e)
        if "wasn't fully snapshotted - cannot restore" in error_message:
            print(f"Cannot restore '{index_name}' from snapshot '{snapshot_name}': Index wasn't fully snapshotted.")

        else:
            print(f"Error restoring snapshot: {error_message}")

if __name__ == '__main__':

    load_dotenv('.env')
    es_url = os.environ['ES_URL']
    es_password = os.environ['ES_PASSWORD']
    es_user = os.environ['ES_USER']
    snapshot_name = os.environ['SNAPSHOT_NAME']
    repository_name = os.environ['REPOSITORY_NAME']

    es = Elasticsearch(hosts=es_url)
    es_client = es.options(basic_auth=(es_user, es_password))
    es_client.info()

    red_indices = es_client.cat.indices(health="red", format="json")
    red_close_indices = []
    for item in red_indices:
        index_name = item["index"]
        index_status = item["status"]

        # ignore close index
        if index_status == "close":
            # try to restore the index
            red_close_indices.append(index_name)
            continue
        
        # Query the index's settings and data stream information
        index_info = es_client.indices.get(index=index_name)

        # Extract the settings, lifecycle status, and data stream information
        if "lifecycle" in index_info[index_name]['settings']['index']:
            lifecycle = index_info[index_name]['settings']['index']['lifecycle']
            rollover_alias = None
            if "rollover_alias" in lifecycle:
                rollover_alias = lifecycle["rollover_alias"]

            index_complete = None 
            if "indexing_complete" in lifecycle:
                index_complete = lifecycle['indexing_complete']
            if index_complete == 'true':
                if rollover_alias != None:
                    index_name = rollover_alias
                close_index(index_name)
        else:
            # check if the index belongs to a datastream
            if "data_stream" in index_info[index_name]:
                data_stream_name = index_info[index_name]["data_stream"]

                # if data_stream_name != "":
                #     response = es_client.indices.rollover(alias=data_stream_name)
                #     # Check the response and handle success
                #     if response.get('acknowledged'):
                #         print(f"Rollover of data stream '{data_stream_name}' successful.")
                #     else:
                #         print(f"Rollover of data stream '{data_stream_name}' not acknowledged.")
            else:
                # it is a regular index
                print(f"{index_name} does not managed by data_stream")
                # response = es_client.indices.rollover(index_name) 
                # if response.get('acknowledged'):
                #     print(f"Rollover of index '{index_name}' successful.")
                # else:
                #     print(f"Rollover of index '{index_name}' not acknowledged.")
    if len(red_close_indices) > 0:
        for close_index in red_close_indices:
            restore_index(close_index, snapshot_name)
    else:
        print("There is no closed red indices.")


