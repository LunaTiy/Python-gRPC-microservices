import os

import grpc
from flask import Flask, render_template

from recommendations_pb2 import RecommendationRequest, RecommendationResponse
from recommendations_pb2_grpc import RecommendationsStub

app = Flask(__name__)

recommendations_host = os.getenv('RECOMMENDATIONS_HOST', 'localhost')
recommendations_channel = grpc.insecure_channel(f'{recommendations_host}:50051')
recommendations_client = RecommendationsStub(recommendations_channel)


@app.route('/')
def render_homepage():
    recommendations_request = RecommendationRequest(id=1)
    response: RecommendationResponse = recommendations_client.Recommend(recommendations_request)

    return render_template('homepage.html', book=response.book)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
