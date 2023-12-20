# Elasticsearch

Reads:

- [https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-replication.html](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-replication.html)
- [https://www.elastic.co/blog/found-elasticsearch-top-down](https://www.elastic.co/blog/found-elasticsearch-top-down)
- [https://www.elastic.co/blog/found-elasticsearch-from-the-bottom-up](https://www.elastic.co/blog/found-elasticsearch-from-the-bottom-up)
- [https://blog.insightdatascience.com/anatomy-of-an-elasticsearch-cluster-part-ii-6db4e821b571](https://blog.insightdatascience.com/anatomy-of-an-elasticsearch-cluster-part-ii-6db4e821b571)
- [https://medium.com/geekculture/elasticsearch-internals-4c4c9ec077fa](https://medium.com/geekculture/elasticsearch-internals-4c4c9ec077fa)
- [https://joshua-robinson.medium.com/thawing-the-elasticsearch-frozen-tier-31a19959dfc4](https://joshua-robinson.medium.com/thawing-the-elasticsearch-frozen-tier-31a19959dfc4)


## Some useful APIs

[http://elasticsearch-cheatsheet.jolicode.com](http://elasticsearch-cheatsheet.jolicode.com)

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
