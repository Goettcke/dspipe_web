FROM tiangolo/uwsgi-nginx-flask:python3.8

EXPOSE 50050
COPY ./app /app
RUN python -m pip install --upgrade pip
RUN python -m pip install -r /app/requirements.txt
RUN python -m pip install /app/DS_Pipe-0.0.2-py3-none-any.whl
#RUN python -m grpc_tools.protoc --experimental_allow_proto3_optional -I /app/protobufs --python_out=/app/app/ \
#           --grpc_python_out=. /app/protobufs/ds_pipe_task.proto

