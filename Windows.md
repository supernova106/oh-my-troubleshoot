# Windows

## ENV

1. Set or print an environment variable

```ps
$env:<VAR_NAME>
```

2. Add a new file using built-in Power Shell function: `New-Item <new_file>`

## Powershell

1. Tail a log file

```ps
 Get-Content $env:ProgramData\Amazon\SSM\Logs\amazon-ssm-agent.log -Wait -Tail 30
```

2. list a directory

```ps
ls <dir_path>
```

3. Test connectivity

```ps
Test-NetConnection ssm.RegionID.amazonaws.com -port 443
Test-NetConnection ec2messages.RegionID.amazonaws.com -port 443
Test-NetConnection ssmmessages.RegionID.amazonaws.com -port 443
```

4. Retrieve a service's dependencies

```ps
Get-Service -Name 'p4prometheus' | Select-Object -ExpandProperty ServicesDependedOn
```

