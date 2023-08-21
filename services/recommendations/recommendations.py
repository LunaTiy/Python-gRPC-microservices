from concurrent import futures
from signal import signal, SIGTERM

import grpc

import recommendations_pb2_grpc
from recommendations_pb2 import RecommendationResponse


class RecommendationService(recommendations_pb2_grpc.RecommendationsServicer):
    def Recommend(self, request, context):
        return RecommendationResponse(book='test')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    recommendations_pb2_grpc.add_RecommendationsServicer_to_server(RecommendationService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()

    def handle_sigterm(*_):
        print("Received shutdown signal")
        all_rpcs_done_event = server.stop(30)
        all_rpcs_done_event.wait(30)
        print("Shut down gracefully")

    signal(SIGTERM, handle_sigterm)
    print("server recommendations started")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
