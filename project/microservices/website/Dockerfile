FROM tiangolo/uwsgi-nginx-flask:python3.8
# FROM python:3.8.7-slim

# changed the workdir from service to app
#RUN mkdir /app
COPY protobufs/ /service/protobufs/
COPY website/ /service/website

WORKDIR /service/website
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN python -m pip install DS_Pipe-0.0.2-py3-none-any.whl
RUN python -m grpc_tools.protoc --experimental_allow_proto3_optional -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/ds_pipe_task.proto

EXPOSE 80
ENV FLASK_APP=app.py
ENTRYPOINT [ "flask", "run", "--port=80"]

