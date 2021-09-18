# Kubernetes

## Kubectl

```sh
kubectl get events --sort-by='.lastTimestamp'
```

- capacity memory

```sh
kubectl get no -o json | jq -r '.items | sort_by(.status.capacity.memory)[]|[.metadata.name,.status.capacity.memory]'
```

- allocatable = [Node Capacity] - [Kube REserved] - [System Reserved] - [Hard-Eviction-Threshold]`
- allocable memory

```sh
kubectl get no -o json | jq -r '.items | sort_by(.status.allocatable.memory)[]|[.metadata.name,.status.allocatable.memory]'
```

- get nodes specs

```sh
kubectl get nodes -o json | jq '.items[].spec'
```

- allocable CPU

```sh
kubectl get no -o json | jq -r '.items | sort_by(.status.allocatable.cpu)[]|[.metadata.name,.status.allocatable.cpu]'
```

- Node Usage

```sh
alias util='kubectl get nodes --no-headers | awk '\''{print $1}'\'' | xargs -I {} sh -c '\''echo {} ; kubectl describe node {} | grep Allocated -A 5 | grep -ve Event -ve Allocated -ve percent -ve -- ; echo '\'''
```

- Cluster wide allocations

```sh
kubectl get po --all-namespaces -o=jsonpath="{range .items[*]}{.metadata.namespace}:{.metadata.name}{'\n'}{range .spec.containers[*]}  {.name}:{.resources.requests.cpu}{'\n'}{end}{'\n'}{end}"
```

- check etcd health

```sh
kubectl get --raw=/healthz/etcd
```

- sort pods by number of restarts

```sh
kubectl get pods --sort-by="{.status.containerStatuses[:1].restartCount}"
```

- find role associated to a service account

```sh
kubectl get rolebindings,clusterrolebindings \
  --all-namespaces  \
  -o custom-columns='KIND:kind,NAMESPACE:metadata.namespace,NAME:metadata.name,SERVICE_ACCOUNTS:subjects[?(@.kind=="ServiceAccount")].name' | grep "<SERVICE_ACCOUNT_NAME>"
```

## Nginx Ingress Controller

- [Nginx Ingress Controller](https://kubernetes.github.io/ingress-nginx/troubleshooting/)


## CoreDNS

Kubernetes DNS Record format
For services: `my-svc.my-namespace.svc.cluster-domain.example`
For example, test1-service.default.svc.cluster.local

For pods: `pod-ip-address.my-namespace.pod.cluster-domain.example.`
For example, if a pod in the default namespace has the IP address 172.17.0.3, and the domain name for your cluster is cluster.local, then the Pod has a DNS name:

`172-17-0-3.default.pod.cluster.local.`

DNS policies can be set on a per-pod basis. Currently Kubernetes supports the following pod-specific DNS policies. These policies are specified in the `dnsPolicy` field of a Pod Spec. If DNS Policy is not specified, "ClusterFirst" will be used

- "Default": The Pod inherits the name resolution configuration from the node that the pods run on. See related discussion for more details.
- "ClusterFirst": Any DNS query that does not match the configured cluster domain suffix, such as "www.kubernetes.io", is forwarded to the upstream nameserver inherited from the node. Cluster administrators may have extra stub-domain and upstream DNS servers configured. See related discussion for details on how DNS queries are handled in those cases.
- "ClusterFirstWithHostNet": For Pods running with hostNetwork, you should explicitly set its DNS policy "ClusterFirstWithHostNet".
- "None": It allows a Pod to ignore DNS settings from the Kubernetes environment. All DNS settings are supposed to be provided using the dnsConfig field in the Pod Spec.

### Default lookup flow

If dnsPolicy is set to “ClusterFirst”, then DNS queries will be sent to the kube-dns service. Queries for domains rooted in the configured cluster domain suffix (any address ending in “.cluster.local” in the example above) will be answered by the kube-dns service. All other queries (for example, www.kubernetes.io) will be forwarded to the upstream nameserver inherited from the node.

The below config tells coredns to use kubernetes plugin for DNS resolution.

#### Kubernetes Plugin

- pods insecure: Always return an A record with IP from request (without checking k8s). This option is provided for backward compatibility with kube-dns.
- ttl allows you to set a custom TTL for responses. The default is 5 seconds. The minimum TTL allowed is 0 seconds, and the maximum is capped at 3600 seconds. Setting TTL to 0 will prevent records from being cached.
- fallthrough [ZONES…] If a query for a record in the zones for which the plugin is authoritative results in NXDOMAIN, normally that is what the response will be. However, if you specify this option, the query will instead be passed on down the plugin chain, which can include another plugin to handle the query. If [ZONES…] is omitted, then fallthrough happens for all zones for which the plugin is authoritative. If specific zones are listed (for example in-addr.arpa and ip6.arpa), then only queries for those zones will be subject to fallthrough.

#### Forward Plugin

forward plugin to implement a stubDomain that forwards DNS query to upstream nameservers

#### Cache Plugin

```
cache [TTL] [ZONES...] {
    success CAPACITY [TTL] [MINTTL]
    denial CAPACITY [TTL] [MINTTL]
    prefetch AMOUNT [[DURATION] [PERCENTAGE%]]
    serve_stale [DURATION]
}
```

- TTL is set to 3600
- success, override the settings for caching successful responses. CAPACITY indicates the maximum number of packets we cache before we start evicting (randomly). TTL overrides the cache maximum TTL. MINTTL overrides the cache minimum TTL (default 5), which can be useful to limit queries to the backend.
- denial, override the settings for caching denial of existence responses. CAPACITY indicates the maximum number of packets we cache before we start evicting (LRU). TTL overrides the cache maximum TTL. MINTTL overrides the cache minimum TTL (default 5), which can be useful to limit queries to the backend. There is a third category (error) but those responses are never cached.
- prefetch will prefetch popular items when they are about to be expunged from the cache. Popular means AMOUNT queries have been seen with no gaps of DURATION or more between them. DURATION defaults to 1m. Prefetching will happen when the TTL drops below PERCENTAGE, which defaults to 10%, or latest 1 second before TTL expiration. Values should be in the range [10%, 90%]. Note the percent sign is mandatory. PERCENTAGE is treated as an int.


