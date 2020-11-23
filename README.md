## django-transfer

### Development

Run locally:

```sh
$ docker build -t web:latest .
$ docker run -d --name django-transfer -e "PORT=8765" -e "DEBUG=1" -p 8007:8765 web:latest
```

Verify [http://localhost:8007/ping/](http://localhost:8007/ping/) works as expected:

```json
{
  "ping": "pong!"
}
```

Stop then remove the running container once done:

```sh
$ docker stop django-transfer
$ docker rm django-transfer
```

### Production

See the blog [post](https://testdriven.io/blog/deploying-django-to-heroku-with-docker/).
