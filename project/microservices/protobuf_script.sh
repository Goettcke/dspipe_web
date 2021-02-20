cd website/
python -m grpc_tools.protoc -I ../protobufs/ --python_out=. --grpc_python_out=. ../protobufs/ds_pipe_task.proto

cd ../runner/
python -m grpc_tools.protoc -I ../protobufs --python_out=. --grpc_python_out=. ../protobufs/ds_pipe_task.proto

cd ../result_castle/
python -m grpc_tools.protoc -I ../protobufs --python_out=. --grpc_python_out=. ../protobufs/ds_pipe_task.proto
