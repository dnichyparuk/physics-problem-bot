FROM python:3.10-slim

LABEL maintainer="Dzmitry Nichyparuk"

# OpenMP library needed by some ML/AI Python packages
RUN apt-get update

COPY requirements.txt /app/

RUN pip install --upgrade pip \
 && pip install --upgrade --no-cache-dir -r /app/requirements.txt

COPY ./src /app
WORKDIR /app

#RUN chainlit create-secret | grep ^CHAINLIT_AUTH_SECRET=.*$ > .env

EXPOSE 8000

ENV PYTHONPATH "${PYTHONPATH}:/app"

CMD ["chainlit", "run", "/app/chainlit_app.py", "-h"]