from concurrent import futures
import random
import grpc

from ds_pipe.datasets.dataset_loader import Dataset_Collections
from ds_pipe.evaluation.evaluation_methods import random_sampling_evaluator
from ds_pipe.semi_supervised_classifiers.kNN_LDP import kNN_LDP
from sklearn.semi_supervised import LabelSpreading, LabelPropagation



from ds_pipe_task_pb2 import (
   Task_Results
)

import ds_pipe_task_pb2_grpc
dc = Dataset_Collections()
dc_full_dict = dc.get_full_dictionary()


class RunnerService(ds_pipe_task_pb2_grpc.RunnerServicer):
    def RunTask(self, request, context):
        print("Calling run task")
        print("Initializing algorithm")
        if request.algorithm == "knn_ldp":
            algorithm = kNN_LDP(n_neighbors = request.n_neighbors)

        elif request.algorithm == "lp_knn":
            algorithm = LabelPropagation(n_neighbors=request.n_neighbors)

        elif request.algorithm == "lp_rbf":
            algorithm = LabelPropagation(gamma=request.gamma)

        elif request.algorithm == "ls_knn":

            algorithm = LabelPropagation(n_neighbors=request.n_neighbors)

        elif request.algorithm == "ls_rbf":
            algorithm = LabelSpreading(gamma=request.gamma, alpha=request.alpha)

        else:
            raise Exception("Unsupported algorithm - knn_ldp, lp and ls is currently the only supported algorithms")


        print("Initialized the algorithm correctly")
        if request.evaluation_method == "random_sampling":
            results = random_sampling_evaluator(dc_full_dict[request.dataset_name], algorithm,
                                        percentage_labelled=request.percent_labelled,
                                        number_of_samples=request.number_of_samples,
                                        quality_measure=request.quality_measure)

        print(f"results: {results}")
        return Task_Results(results=results)

def serve():
    print("Server up and running!")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ds_pipe_task_pb2_grpc.add_RunnerServicer_to_server(
        RunnerService(), server
    )

    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
