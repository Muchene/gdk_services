FROM python:3.10


WORKDIR /opt/aramse/mailagent
COPY api.py /opt/aramse/mailagent/
COPY requirements.txt /opt/aramse/mailagent/

ENV PYTHONPATH "${PYTHONPATH}:/opt/aramse"
RUN pip3 install -r requirements.txt

CMD [ "python3 api.py" ]

