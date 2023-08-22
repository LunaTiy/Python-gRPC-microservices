import random
from concurrent import futures
from signal import signal, SIGTERM

import grpc

import recommendations_pb2_grpc
from recommendations_pb2 import RecommendationResponse
from models import Books
from sa_utils import session_scope


class RecommendationService(recommendations_pb2_grpc.RecommendationsServicer):
    def Recommend(self, request, context):
        with session_scope() as s:
            books: list[Books] = s.query(Books).filter(Books.category_id == request.category_id).all()
            if len(books) == 0:
                return RecommendationResponse()

        book: Books = random.choice(books)
        print(f"Book: {book.book_name}")
        return RecommendationResponse(book=book.book_name)


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
