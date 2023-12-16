FROM python:3.12

WORKDIR /app

#COPY noteman /app
COPY pyproject.toml /app
#RUN cd /app

RUN pip install Django
RUN pip install build
#RUN python -m build
