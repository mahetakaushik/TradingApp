FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /TradingApp/src
COPY requirements.txt /TradingApp/src/
RUN pip install -r requirements.txt
COPY . /TradingApp/src/