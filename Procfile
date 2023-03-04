release: python manage.py migrate
web: uvicorn storefront.asgi:application
worker: celery -A storefront worker
