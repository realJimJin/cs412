# Deploying mini_insta to Render

This repo contains multiple Django apps. This deployment targets **mini_insta only**.

## Entry points

- Settings: `cs412/settings.py`
- WSGI: `cs412/wsgi.py`
- Root URLs: `cs412/urls.py` (configured so `/` serves `mini_insta`)

## Render environment variables

Required:

- `SECRET_KEY` = a long random string
- `DEBUG` = `0`

Recommended:

- `PUBLIC_URL` = `https://<your-service>.onrender.com`

Optional:

- `ALLOWED_HOSTS` = `<your-service>.onrender.com` (comma-separated)
- `DATABASE_URL` (Postgres; otherwise SQLite is used)

## Render commands

### Build Command

```bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
```

### Start Command

```bash
gunicorn cs412.wsgi:application
```

## Notes

- Static files are served via WhiteNoise.
- Media uploads are not persisted on Render’s ephemeral filesystem unless you use external storage.
