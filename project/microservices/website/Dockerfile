FROM python:3.8.7-slim

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

EXPOSE 5000
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

ENTRYPOINT [ "flask", "run"]

