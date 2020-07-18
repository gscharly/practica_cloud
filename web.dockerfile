FROM python:3.6
COPY requirements_app.txt requirements.txt
RUN pip install -r requirements.txt
ADD . /todo
WORKDIR /todo
CMD ["python", "app.py"]