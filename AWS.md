# AWS

- Get instance id from host

```sh
#!/bin/bash

node_ip=$(dig +short ${HOST})
node_instance_id=$(aws ec2 describe-instances --filters "Name=private-ip-address,Values=${node_ip}" --region us-west-2 | jq -r '.Reservations[0].Instances[0].InstanceId')
```

## ECS

- get container instance recommended AMI

```sh
aws --region us-west-2 ssm get-parameters --names /aws/service/ecs/optimized-ami/amazon-linux-2/recommended | jq -r .Parameters[0].Value | jq -r .image_id
```
