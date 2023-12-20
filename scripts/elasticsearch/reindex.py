# tested again ES 8.x 
from elasticsearch import Elasticsearch
import requests
import time
import threading
import os
from dotenv import load_dotenv

def reindex(es_client, src_index, dest_index="", index_to_copy="", require_rollover=False):

    context = es_client.indices.get(index=src_index)
    datastream = context[src_index].get("data_stream")

    if dest_index == "":
        next_index = 2
        dest_index = f"{src_index}.{next_index}"

    ######################################################################################################
    # STEP 2. ROLLOVER EXISTING INDEX                                                                    #
    # ----------------------------------------------------------------------------------------------------#
    # make sure the new mapping is applied and confident it is working as expected
    # index rollover will automatically create a new active index where the latest logs will be stored in
    if index_to_copy != "":
        index_context = (es_client.indices.get(index=index_to_copy))[index_to_copy]
        if index_context:
            print(f"copying latest index mapping from {index_to_copy}")
        else:
            print(
                f"{index_to_copy} - unable to find latest working index for this datastream"
            )
            return

    if require_rollover == False:
        ds_context = es_client.indices.get_data_stream(name=datastream)
        ds_indices = ds_context["data_streams"][0].get("indices")
        latest_index = ds_indices[len(ds_indices) - 1]["index_name"]
        if latest_index:
            print(f"copying latest index mapping from {latest_index}")
            index_context = (es_client.indices.get(index=latest_index))[latest_index]
        else:
            print(f"unable to find latest working index for this datastream")
            return
    else:
        rollover = requests.post(
            kibana_url + f"/{datastream}/_rollover", auth=(es_user, es_password)
        )
        new_live_index = rollover.json()["new_index"]
        # this step will retrieve the index mapping from the newly rolled over index
        index_context = (es_client.indices.get(index=new_live_index))[new_live_index]

    ######################################################################################################
    # STEP 3. CREATE A NEW INDEX WITH THE NEW MAPPING TO MIGRATE THE OLD DATA TO
    # ----------------------------------------------------------------------------------------------------#
    def create_clone_index(index_name, shards, replicas, mapping, total_field_limits):
        settings = {
            "number_of_shards": shards,
            "number_of_replicas": replicas,
            "index.mapping.total_fields.limit": total_field_limits,
        }

        es_client.indices.create(index=index_name, settings=settings, mappings=mapping)

    create_clone_index(
        index_name=dest_index,
        shards=index_context["settings"]["index"]["number_of_shards"],
        replicas=index_context["settings"]["index"]["number_of_replicas"],
        mapping=index_context["mappings"],
        total_field_limits=10000,
    )

    # next_index = 2
    # dest_index = f"{index}.{next_index}"
    # create_status = False
    # while create_status == False:
    #     try:
    #         response = create_clone_index(dest_index,shards=index_context['settings']['index']['number_of_shards'], replicas=index_context['settings']['index']['number_of_replicas'], mapping=index_context['mappings'], total_field_limits=10000)
    #         if response.get('acknowledged') == None:
    #             if response.get('error') and response['error']['root_cause'][0].get('type') == 'resource_already_exists_exception':
    #                 create_status = False
    #         elif response.get('acknowledged') == True:
    #             create_status = True
    #             print('Index created Successfully: {}'.format(response.get('index')))
    #     except es_client.ElasticsearchException as es1:
    #         return print(f"Error creating new index: {es1}")
    ######################################################################################################
    # STEP 4. START THE REINDEXING PROCESS                                                               #
    # ----------------------------------------------------------------------------------------------------#

    reindex = es_client.reindex(
        source={"index": src_index},
        dest={"index": dest_index},
        wait_for_completion=False,
    )

    task_id = reindex.get("task")
    task = es_client.tasks.get(task_id=task_id)
    print("Reindex Task ID: {}".format(task_id))

    created = task.body["task"]["status"].get("created")
    total = int((es_client.count(index=src_index)).body["count"])

    while task_id == None or created == None:
        task_id = reindex.get("task")
        task = es_client.tasks.get(task_id=task_id)
        created = task.body["task"]["status"].get("created")

    ######################################################################################################
    # STEP 5. MONITORING THE REINDEXING PROCESS FOR COMPLETION
    # ----------------------------------------------------------------------------------------------------#

    status = task.body["completed"]

    while status == False:
        task = es_client.tasks.get(task_id=task_id)
        status = task.body["completed"]
        created = task.body["task"]["status"].get("created")
        description = task.body["task"].get("description")
        print(f"{task_id}:{status}:{created}-{total}:{description}")
        time.sleep(10)

    ######################################################################################################
    # STEP 6. ADD NEW REINDEX INDEX TO THE BACKING DATASTREAM
    # ----------------------------------------------------------------------------------------------------#
    # Be sure the reindexing process is complete, the data within the new index is not searchable until it is added to the backing index/datastream.

    if created == total:
        action = {
            "add_backing_index": {
                "data_stream": datastream,
                "index": dest_index,
            }
        }
        es_client.indices.modify_data_stream(actions=action)

        index_status = "yellow"
        while index_status != "green":
            index_stats = es_client.indices.stats(index=dest_index)
            index_status = index_stats["indices"][dest_index]["health"]

        print(
            f"Index status: {index_status}: Reindex successful will now delete old index"
        )
        es_client.indices.delete(index=src_index)
    else:
        print("Task completed without copying all documents to new index")

def main(es_client, src_indices):

    processes = []
    for i in src_indices:
        # Apply each integration policy in a separate thread
        process = threading.Thread(target=reindex, args=(es_client, i,))
        process.start()
        processes.append(process)

    for process in processes:
        # Wait for all the threads to finish before proceeding
        process.join()

if __name__ == "__main__":
    load_dotenv('.env')
    kibana_url = os.environ['ES_URL']
    es_password = os.environ['ES_PASSWORD']
    es_user = os.environ['ES_USER']
    es = Elasticsearch(hosts=kibana_url)
    es_client = es.options(basic_auth=(es_user, es_password))
    es_client.info()
    
    src_indices = [
        ".ds-logs-example-test1-2021.12.19-000024"
    ]
    main(es_client, src_indices)
