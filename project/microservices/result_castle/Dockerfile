FROM python:3.8.7-slim

RUN mkdir /service
COPY protobufs/ /service/protobufs/
COPY result_castle/ /service/result_castle/
WORKDIR /service/result_castle
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN python -m grpc_tools.protoc --experimental_allow_proto3_optional -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/ds_pipe_task.proto

EXPOSE 50051
EXPOSE 50050
ENTRYPOINT [ "python", "result_castle.py"]