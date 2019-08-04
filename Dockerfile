FROM python:3.6

WORKDIR /opt/services/sec-workshop/djangoapp
COPY djangoapp /opt/services/sec-workshop/djangoapp/
RUN pip install -r conf/requirements.txt
RUN python manage.py collectstatic --no-input --settings base.settings
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--settings", "base.settings"]