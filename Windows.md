# Windows

## Powershell

1. Tail a log file

```ps
 Get-Content $env:ProgramData\Amazon\SSM\Logs\amazon-ssm-agent.log -Wait -Tail 30
```

2. list a directory

```ps
ls <dir_path>
```
