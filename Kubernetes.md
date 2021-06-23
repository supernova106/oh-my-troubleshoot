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
