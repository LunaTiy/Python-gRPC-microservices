import logging
import random
import socket
from concurrent import futures
from signal import signal, SIGTERM

import grpc

import recommendations_pb2_grpc
from models import Books
from recommendations_pb2 import RecommendationResponse
from sa_utils import session_scope

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)


def init_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
    return logger


class RecommendationService(recommendations_pb2_grpc.RecommendationsServicer):
    logger = init_logger()

    def Recommend(self, request, context):
        with session_scope() as s:
            self.logger.debug(
                f"Hostname: {hostname} with ip: {ip_address} get request with category id: {request.category_id}")
            books: list[Books] = s.query(Books).filter(Books.category_id == request.category_id).all()
            if len(books) == 0:
                self.logger.debug("Empy result from db")
                return RecommendationResponse()

        book: Books = random.choice(books)
        self.logger.debug(f"Selected book: {book.id} - {book.book_name}")
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
