FROM python:3.12-slim
RUN pip install --upgrade pip
EXPOSE 4000
WORKDIR /fl_api
COPY ./Flask_app .
RUN pip install -r  requirements.txt

COPY run.sh .

RUN chmod +x run.sh
CMD ["./run.sh"]
