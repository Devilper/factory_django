FROM python:3.8

RUN mkdir /code

COPY . /code

WORKDIR /code

RUN pip3 install --upgrade pip
RUN pip3 install -r requirement.txt -i https://pypi.doubanio.com/simple

CMD ["gunicorn", "-b", "0.0.0.0:8000", "--workers=4", "--timeout=120", "--access-logfile", "-", "factory_django.wsgi"]

