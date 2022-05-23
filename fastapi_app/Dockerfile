FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/fastapi_app

CMD ["uvicorn", "fastapi_app.main:app", "--host", "0.0.0.0", "--port", "80"]
