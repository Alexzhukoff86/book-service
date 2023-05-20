from concurrent import futures

import grpc

from utils import logger
from utils.config import Config

import protopy.book_pb2 as pb
import protopy.book_pb2_grpc as rpc

from grpc_reflection.v1alpha import reflection

from services.book_service import BookService


def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc.add_BookServiceServicer_to_server(
        BookService(), server
    )
    names = (
        pb.DESCRIPTOR.services_by_name['BookService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(names, server)
    logger.info(f"Run book server on {Config.book_server}:{Config.book_server_port}")
    #server.add_insecure_port(f"{Config.book_server}:{Config.book_server_port}")
    server.add_insecure_port("localhost:50052")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    server()
