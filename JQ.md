# JQ

## Select a particular key from a list

```sh
jq ".[] | select(.key | contains(\"${value}\"))"
```
