# Elasticsearch

## Some useful APIs

1. Index statistics. The API is only intended for human use

```sh
GET _cat/indices?h=health,status,index,id,pri,rep,docs.count,docs.deleted,store.size,creation.date.string&v=
```

2. Get unhealthy indices

```sh
GET _cat/indices?v&health=red&h=index,status,health
```

3. Show shards recovery activities

```sh
GET _cat/recovery?v&active_only=true
```

4. Explain cluster shard allocation

```sh
GET /_cluster/allocation/explain
```

5. Get setting of an index

```sh
GET <INDEX>?features=settings&flat_settings
```

6. Set max scroll

```sh
PUT _cluster/settings
{
    "persistent" : {
        "search.max_open_scroll_context": 2048
    },
    "transient": {
        "search.max_open_scroll_context": 2048
    }
}
```
