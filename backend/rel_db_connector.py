from relational_database.relational_tables import User, Chat
from relational_database.relational_database import Session
from typing import Any, Callable

class RelDBConnector():
    
    session = Session()

    def __init__(self) -> None:
        pass

    def commit_session(self, func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            func(*args, **kwargs)
            self.session.commit()
            # self.session.close()
        return wrapper

    # Create new user
    @commit_session
    def register_user(self, id: int, username: str):
        self.session.add(User(id, username))


    # Create new chat
    @commit_session
    def open_new_chat(self, id: int):
        self.session.add(Chat(id))
