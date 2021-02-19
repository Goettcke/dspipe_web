from concurrent import futures
import random
import grpc
import os
import ast
import threading

from ds_pipe_task_pb2_grpc import RunnerStub
from ds_pipe_task_pb2 import (
    Task_Results,
    Task
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
    def call_runner(self, request):
        try:
            runners_response = runners_client.Run_task(request)
            result = runners_response.results

        except Exception as e:
            print(e)
            print("Aww why this no work")

        return result


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
            """
            If the database doesn't contain the result, we have to compute it by calling a remote, however, we want to respond immediately, so the website, can get on with it's life.
            """
            x = threading.Thread(target=self.run_request, args=(request,))
            x.start()
            result = [0.42]
        else:
            print("Result lies in the database")
            print(query_list[0].result)
            result = ast.literal_eval(query_list[0].result)

        session.commit()
        session.close()
        return result

    def run_request(self, request):
        # rewrite to threading
        conn = engine.connect()
        session = Session(bind=conn)
        result = [-42]
        query_list = [-42]

        result = self.call_runner(request)

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

        session.commit()
        session.close()

    def Evaluate_Task(self, request, context):
        results = [-42]
        try:
            results = self.find_request(request)

        except Exception as e:
            print(e)
            print("Some shit happened")

        return Task_Results(results=results)

    # CamelCased to denote RPC call
    def ResultResponse(self, request, context):
        conn = engine.connect()
        session = Session(bind=conn)

        if request.algorithm_name == "knn_ldp":
            session_query = session.query(Knn_ldp)

        elif request.algorithm_name == "lp_knn":
            session_query = session.query(Lp_knn)

        elif request.algorithm_name == "ls_knn":
            session_query = session.query(Ls_knn)

        elif request.algorithm_name == "lp_rbf":
            session_query = session.query(Lp_rbf)

        elif request.algorithm_name == "ls_rbf":
            session_query = session.query(Ls_rbf)

        else:
            print("Incorrect table called through remote request")


        query_result = session_query.filter_by(id=request.result_id).first()
        result = ast.literal_eval(query_result.result)
        session.commit()
        session.close()
        return result

    # CamelCased to denote RPC call
    def ConfigurationResponse(self, request, context):
        conn = engine.connect()
        session = Session(bind=conn)

        if request.algorithm_name == "knn_ldp":
            session_query = session.query(Knn_ldp)

        elif request.algorithm_name == "lp_knn":
            session_query = session.query(Lp_knn)

        elif request.algorithm_name == "ls_knn":
            session_query = session.query(Ls_knn)

        elif request.algorithm_name == "lp_rbf":
            session_query = session.query(Lp_rbf)

        elif request.algorithm_name == "ls_rbf":
            session_query = session.query(Ls_rbf)

        else:
            print("Incorrect table called through remote request")


        query_result = session_query.filter_by(id=request.result_id).first()


        get_alpha = lambda alg: query_result.alpha if alg == "ls_rbf" else 0
        get_gamma = lambda alg: query_result.gamma if (alg == "ls_rbf" or alg == "lp_rbf") else 0
        get_n_neighbors = lambda alg: query_result.n_neighbors if (alg == "ls_knn" or alg == "lp_knn" or alg=="knn_ldp") else 0


        task_configuration = Task(user_id=0,
             algorithm=request.algorithm,
             number_of_samples=query_result.number_of_samples,
             dataset_name = query_result.dataset,
             n_neighbors = get_n_neighbors(request.algorithm),
             quality_measure = query_result.quality_measure,
             percent_labelled = query_result.percent_labelled,
             alpha = get_alpha(request.algorithm),
             gamma = get_gamma(request.algorithm),
             evaluation = query_result.evaluation_method
             )

        session.commit()
        session.close()

        return task_configuration



def serve():
    print("Server up and running!")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ds_pipe_task_pb2_grpc.add_Task_EvaluatorServicer_to_server(
        ResultCastleService(), server
    )

    server.add_insecure_port("[::]:50050")
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
