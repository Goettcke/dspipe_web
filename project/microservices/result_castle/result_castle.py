from concurrent import futures
import grpc
import os
import ast
import threading
from random import randint

from ds_pipe_task_pb2_grpc import RunnerStub
from ds_pipe_task_pb2 import (
    Task_Results,
    Task,
    Has_Results_Response,
    Alg_Id
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
        result = -1
        try:
            runners_response = runners_client.RunTask(request)
            result = runners_response.results

        except Exception as e:
            print(e)
            print("Unfortunately the request couldn't execute")

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
        has_result = False
        pink_slip = 0
        id = 0
        print(f"The requested algorithm: {request.algorithm}")
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

            print("Result is not in the database - sending compute request to runner")
            pink_slip = self.generate_pink_slip()
            x = threading.Thread(target=self.run_request, args=(request,pink_slip,))
            x.start()
            has_result = False
        else:

            print("Result lies in the database")
            has_result = True
            id = query_list[0].id
            #print(query_list[0].result)
            #result = ast.literal_eval(query_list[0].result)

        session.commit()
        session.close()
        return has_result, pink_slip, id, request.algorithm

    def run_request(self, request, pink_slip):
        conn = engine.connect()
        session = Session(bind=conn)
        result = [-42]
        query_list = [-42]

        result = self.call_runner(request)
        if result != -1: # Ensuring we don't insert garbage into the db!

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
                                        result=str(result),
                                        pink_slip=pink_slip
                                        )
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
                                    result=str(result),
                                    pink_slip=pink_slip
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
                                    result=str(result),
                                    pink_slip=pink_slip
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
                                    result=str(result),
                                    pink_slip=pink_slip
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
                                    result=str(result),
                                    pink_slip=pink_slip
                                    )
                    session.add(instance)
                    session.commit()

                except Exception as e:
                    print(e)
                    print("Ahh we didn't get any ls_rbf results from remote :(")

        session.commit()
        session.close()

    def Evaluate_Task(self, request, context):
        has_result = False
        try:
            has_result, pink_slip, id, alg = self.find_request(request)
            print("Got has result")

            if has_result:
                response = Has_Results_Response(has_result = has_result, pink_slip=0, result_id=id, algorithm_name=alg )

            elif has_result == False:
                response = Has_Results_Response(has_result = has_result, pink_slip=pink_slip)


        except Exception as e:
            print(e)
            has_result = None
        return response

    
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
        results = ast.literal_eval(query_result.result)

        session.commit()
        session.close()

        return Task_Results(results=results)

    # CamelCased to denote RPC call
    def ConfigurationResponse(self, request, context):
        print("Running ConfigurationResponse")
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
             algorithm=request.algorithm_name,
             number_of_samples=query_result.number_of_samples,
             dataset_name = query_result.dataset,
             n_neighbors = get_n_neighbors(request.algorithm_name),
             quality_measure = query_result.quality_measure,
             percent_labelled = query_result.percent_labelled,
             alpha = get_alpha(request.algorithm_name),
             gamma = get_gamma(request.algorithm_name),
             evaluation_method = query_result.evaluation_method,
             results = str([round(x, 3) for x in ast.literal_eval(query_result.result)])
             )

        session.commit()
        session.close()

        return task_configuration

    def generate_pink_slip(self):
        pink_slip = -1
        """
        This i-1 stuff, and the loop setup is to avoid the very unlikely event
        that the pink slip is -1 since this is our error code, and the user database entry means,
        that if we set pink slips to -1 establising the pointer, we will never find them in queries.
        """
        while pink_slip == -1:
            pink_slip = randint(-2147483648, 2147483647)
        return pink_slip

    def GetPinkSlipAlgId(self, request, context):
        pink_slip = request.pink_slip
        conn = engine.connect()
        session = Session(bind=conn)
        alg = ""
        id_ = -1
        knn_ldp_query = session.query(Knn_ldp).filter_by(pink_slip = pink_slip).all()
        lp_knn_query = session.query(Lp_knn).filter_by(pink_slip = pink_slip).all()
        ls_knn_query = session.query(Ls_knn).filter_by(pink_slip = pink_slip).all()
        lp_rbf_query = session.query(Lp_rbf).filter_by(pink_slip = pink_slip).all()
        ls_rbf_query = session.query(Ls_rbf).filter_by(pink_slip = pink_slip).all()

        if knn_ldp_query != []: #Meaning our results were found here
            alg = "knn_ldp"
            id_ = knn_ldp_query[0].id

        elif lp_knn_query != []:
            alg = "lp_knn"
            id_ = lp_knn_query[0].id

        elif ls_knn_query != []:
            alg = "ls_knn"
            id_ = ls_knn_query[0].id

        elif lp_rbf_query != []:
            alg = "lp_rbf"
            id_ = lp_rbf_query[0].id

        elif ls_rbf_query != []:
            alg = "ls_rbf"
            id_ = ls_rbf_query[0].id
        else:
            print("Could't find the pink slip in the database :(  )")

        if id_ == -1 or alg == "":
            print("An unexpected error occurred")
        session.commit()
        session.close()
        response = Alg_Id(id = id_, alg = alg)
        return response



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
