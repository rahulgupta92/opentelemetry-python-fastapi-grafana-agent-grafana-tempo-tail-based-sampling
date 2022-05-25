FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/python_scripts

CMD ["python", "python_scripts/fastapi_server_polling_service.py"]
