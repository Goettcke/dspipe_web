from concurrent import futures
import random
import grpc
import os
import ast

from ds_pipe_task_pb2_grpc import RunnerStub
from ds_pipe_task_pb2 import (
   Task_Results
)

import ds_pipe_task_pb2_grpc
from models import Knn_ldp, Lp_knn, Ls_knn, Ls_rbf, Lp_rbf

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = sqlalchemy.create_engine("sqlite:///db.sqlite",echo=True)


# Setting up supported algorithms

# Setting up the path to runners environment
runners_host = os.getenv("RUNNERS_HOST", "localhost")
runners_channel = grpc.insecure_channel(f"{runners_host}:50051")
runners_client = RunnerStub(runners_channel)

# Setting up the database
Session = sessionmaker()
Session.configure(bind=engine)


class ResultCastleService(ds_pipe_task_pb2_grpc.Task_EvaluatorServicer):

    def get_query_list(self,session_query, request, parameters):
        """

        Keyword Arguments:
        session_query: Is a sqlalchemy session.query object
        request:  is a gRPC request
        parameters: is a list containing the parameters e.g. ["n_neighbors"]
        """
        if "n_neighbors" in parameters:
            query_list = session_query.filter_by(dataset=request.dataset_name,
                                        number_of_samples=request.number_of_samples,
                                        percent_labelled=request.percent_labelled,
                                        n_neighbors=request.n_neighbors,
                                        quality_measure=request.quality_measure,
                                        evaluation_method=request.evaluation_method).all()
        elif "gamma" in parameters and "alpha" not in parameters:
            query_list = session_query.filter_by(dataset=request.dataset_name,
                                        number_of_samples=request.number_of_samples,
                                        percent_labelled=request.percent_labelled,
                                        gamma=request.gamma,
                                        quality_measure=request.quality_measure,
                                        evaluation_method=request.evaluation_method).all()


        elif "gamma" in parameters and "alpha" in parameters:
            query_list = session_query.filter_by(dataset=request.dataset_name,
                                        number_of_samples=request.number_of_samples,
                                        percent_labelled=request.percent_labelled,
                                        gamma=request.gamma,
                                        alpha=request.alpha,
                                        quality_measure=request.quality_measure,
                                        evaluation_method=request.evaluation_method).all()
        else:
            query_list = []

        return query_list

    def find_request(self, request):

        conn = engine.connect()
        session = Session(bind=conn)
        result = [-42]
        query_list = [-42]

        print(f"\n\n\n Vi koerer nu John  \n \n \n ")

        if request.algorithm == "knn_ldp":
            session_query = session.query(Knn_ldp)
            query_list = self.get_query_list(session_query, request, ["n_neighbors"])
        elif request.algorithm == "lp_knn":
            session_query = session.query(Lp_knn)
            query_list = self.get_query_list(session_query, request, ["n_neighbors"])
        elif request.algorithm == "ls_knn":
            session_query = session.query(Ls_knn)
            query_list = self.get_query_list(session_query, request, ["n_neighbors"])

        elif request.algorithm == "lp_rbf":
            session_query = session.query(Lp_rbf)
            query_list = self.get_query_list(session_query, request, ["gamma"])

        elif request.algorithm == "ls_rbf":
            session_query = session.query(Ls_rbf)
            query_list = self.get_query_list(session_query, request, ["gamma", "alpha"])
        else:
            raise Exception("The requested algorithm is not supported")


        if len(query_list) < 1:
            print("Pis os da - den er tom")
            try:
                runners_response = runners_client.Run_task(request)
                result = runners_response.results
            except Exception as e:
                print(e)
                print("Aww why this no work")
            if request.algorithm == "knn_ldp":

                try:
                    # In this case we should make an asynchronous call to runner service.
                    knn_instance = Knn_ldp(
                                        dataset=request.dataset_name,
                                        number_of_samples=request.number_of_samples,
                                        percent_labelled=request.percent_labelled,
                                        n_neighbors=request.n_neighbors,
                                        quality_measure=request.quality_measure,
                                        evaluation_method=request.evaluation_method,
                                        result=str(result))
                    session.add(knn_instance)
                    session.commit()

                except Exception as e:
                    print(e)
                    print("Ahh we didn't get any knn_ldp results from remote :(")
            elif request.algorithm == "lp_knn":

                try:
                    instance = Lp_knn(
                                    dataset=request.dataset_name,
                                    number_of_samples=request.number_of_samples,
                                    percent_labelled=request.percent_labelled,
                                    n_neighbors=request.n_neighbors,
                                    quality_measure=request.quality_measure,
                                    evaluation_method=request.evaluation_method,
                                    result=str(result)
                                    )
                    session.add(instance)
                    session.commit()
                except Exception as e:
                    print(e)
                    print("Ahh we didn't get any lp_knn results from remote :(")

            elif request.algorithm == "ls_knn":
                try:
                    instance = Ls_knn(
                                    dataset=request.dataset_name,
                                    number_of_samples=request.number_of_samples,
                                    percent_labelled=request.percent_labelled,
                                    n_neighbors=request.n_neighbors,
                                    quality_measure=request.quality_measure,
                                    evaluation_method=request.evaluation_method,
                                    result=str(result)
                                    )
                    session.add(instance)
                    session.commit()
                except Exception as e:
                    print(e)
                    print("Ahh we didn't get any ls_knn results from remote :(")


            elif request.algorithm == "lp_rbf":

                try:
                    instance = Lp_rbf(
                                dataset=request.dataset_name,
                                number_of_samples=request.number_of_samples,
                                percent_labelled=request.percent_labelled,
                                gamma=request.gamma,
                                quality_measure=request.quality_measure,
                                evaluation_method=request.evaluation_method,
                                result=str(result)
                                )
                    session.add(instance)
                    session.commit()

                except Exception as e:
                    print(e)
                    print("Ahh we didn't get any lp_rbf results from remote :(")


            elif request.algorithm == "ls_rbf":
                try:
                    instance = Ls_rbf(
                                    dataset=request.dataset_name,
                                    number_of_samples=request.number_of_samples,
                                    percent_labelled=request.percent_labelled,
                                    gamma=request.gamma,
                                    alpha=request.alpha,
                                    quality_measure=request.quality_measure,
                                    evaluation_method=request.evaluation_method,
                                    result=str(result)
                                    )
                    session.add(instance)
                    session.commit()

                except Exception as e:
                    print(e)
                    print("Ahh we didn't get any ls_rbf results from remote :(")


        else:
            print("Der ligger sgu noget i databasen")
            print(query_list[0].result)
            result = ast.literal_eval(query_list[0].result)

        session.commit()
        session.close()
        return result



    def Evaluate_Task(self, request, context):
        results = [-42]
        try:
            results = self.find_request(request)

        except Exception as e:
            print(e)
            print("Some shit happened")
        return Task_Results(results=results)

def serve():
    print("Server up and running!")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ds_pipe_task_pb2_grpc.add_Task_EvaluatorServicer_to_server(
        ResultCastleService(), server
    )

    server.add_insecure_port("[::]:50050") # most likely should be another port, or use some decorator to route the traffic.
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()