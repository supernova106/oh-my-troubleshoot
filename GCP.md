# GCP

## GCLOUD

- get GCE pubIP

```sh
gcloud compute instances describe apache-2 --format 'value(networkInterfaces[0].accessConfigs[0].natIP)'
```
