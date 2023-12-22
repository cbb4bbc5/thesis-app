FROM python:3.12

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
#COPY noteman /app
COPY pyproject.toml /app
#RUN cd /app

COPY requirements.txt .
RUN pip install -r requirements.txt

#RUN pip install Django
#RUN pip install build
#RUN python -m build
