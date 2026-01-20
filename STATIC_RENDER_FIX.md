# Static files for Render (mini_insta)

## Where static files live
- Top-level `static/` directory contains CSS files:
  - `static/style_insta.css` (main CSS for mini_insta)
  - `static/styles.css` (shared)
  - `static/modern.css`
- `mini_insta/` app has **no app/static/** directory.

## How templates reference static
- All templates extend `mini_insta/base.html`
- `base.html` loads `{% load static %}` and references CSS via:
  ```html
  <link rel="stylesheet" href="{% static 'style_insta.css' %}">
  ```
- No hardcoded `/static/` or `css/` paths found.

## Settings (cs412/settings.py)
- `STATIC_URL = '/static/'`
- `STATIC_ROOT = BASE_DIR / 'staticfiles'`
- `STATICFILES_DIRS = [BASE_DIR / 'static']`
- WhiteNoise enabled if installed; uses `whitenoise.storage.CompressedManifestStaticFilesStorage`

## Render commands
- **Build Command**
  ```bash
  pip install -r requirements.txt
  python manage.py collectstatic --noinput
  python manage.py migrate
  ```
- **Start Command**
  ```bash
  gunicorn cs412.wsgi:application
  ```

## Required env vars
- `SECRET_KEY` (set)
- `DEBUG=0` (set)
- `PUBLIC_URL` (recommended for CSRF_TRUSTED_ORIGINS)

## Tests
1. Open `/static/style_insta.css` in browser → should return 200.
2. Inspect network tab → CSS request should be 200, not 404/403.

## Notes
- WhiteNoise serves static files from `staticfiles/` after `collectstatic`.
- No S3/CDN used; static files are bundled with the deploy.
- Media uploads are not persisted on Render’s ephemeral filesystem.
