FROM python

RUN mkdir /service
COPY protobufs/ /service/protobufs/
COPY marketplace/ /service/marketplace/
WORKDIR /service/marketplace
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=.  \
    --grpc_python_out=. --mypy_out=. ../protobufs/recommendations.proto 

EXPOSE 5000

ENTRYPOINT ["flask", "--app", "marketplace.py", "run", "--host=0.0.0.0"]