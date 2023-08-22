import logging
import os
import random
import socket

import grpc
from flask import Flask, render_template

from recommendations_pb2 import RecommendationRequest, RecommendationResponse
from recommendations_pb2_grpc import RecommendationsStub

app = Flask(__name__)

recommendations_host = os.getenv('RECOMMENDATIONS_HOST', 'localhost')
recommendations_channel = grpc.insecure_channel(f'{recommendations_host}:50051')
recommendations_client = RecommendationsStub(recommendations_channel)

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)


def init_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
    return logger

logger = init_logger()


@app.route('/')
def render_homepage():
    logger.debug(f"Hostname: {hostname} with ip: {ip_address} get request from user")
    category = random.randint(1, 3)
    logger.debug(f"Selected category: {category}")

    recommendations_request = RecommendationRequest(category_id=category)
    response: RecommendationResponse = recommendations_client.Recommend(recommendations_request)

    return render_template('homepage.html', book=response.book)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
