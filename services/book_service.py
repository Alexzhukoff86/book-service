import grpc
import protopy.book_pb2 as pb
import protopy.book_pb2_grpc as rpc
from utils import logger

from models.books import BookModel

class BookService(rpc.BookServiceServicer):
    
    def GetBook(self, request, context):
        logger.info(f"Get book request {request}")
        book_sql = BookModel.find_by_title(request.title)
        logger.info(f"Book {book_sql}")
        if not book_sql:
            context.abort(grpc.StatusCode.NOT_FOUND, "Book not found")
        genre = pb.BookGenre.Name(int(book_sql.genre))
        logger.info(f"GENRE {genre}")
        return pb.GetBookResponse(book=pb.Book(id=book_sql.id, genre=genre, title=book_sql.title, count=book_sql.count))

    def UpdateBookCount(self, request, context):
        logger.info(f"Update book count request {request}")
        book_sql = BookModel.fynd_by_id(request.id)
        if not book_sql:
            context.abort(grpc.StatusCode.NOT_FOUND, "Book not found")
        book_sql.count = request.count
        book_sql.save_to_db()
        genre = pb.BookGenre.Name(int(book_sql.genre))
        logger.info(f"GENRE {genre}")
        return pb.UpdateBookCountResponse(book=pb.Book(id=book_sql.id, genre=genre, title=book_sql.title, count=book_sql.count))

    def AddBook(self, request, context):
        logger.info(f"Add new book request {request}")
        book_sql = BookModel(genre=request.genre, title=request.title, count=request.count)
        if BookModel.find_by_title(request.title):
            context.abort(grpc.StatusCode.ALREADY_EXISTS, "Book already exists")
        book_sql.save_to_db()
        genre = pb.BookGenre.Name(int(book_sql.genre))
        return pb.AddBookResponse(book=pb.Book(id=book_sql.id, genre=genre, title=book_sql.title, count=book_sql.count))
