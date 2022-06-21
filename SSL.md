# SSL

1. Get pubcert from TLS endpoint

```sh
openssl s_client -showcerts -connect <HOST>:443 </dev/null | sed -n -e '/-.BEGIN/,/-.END/ p' > certifs.pem
```

2. View pubcert info

```sh
echo | openssl s_client -showcerts -servername gnupg.org -connect <HOST>:443 2>/dev/null | openssl x509 -inform pem -noout -text
```
