# SSL

1. Get pubcert from TLS endpoint

```sh
openssl s_client -showcerts -connect <HOST>:443 </dev/null | sed -n -e '/-.BEGIN/,/-.END/ p' > certifs.pem
```
