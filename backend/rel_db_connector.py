from relational_database.relational_tables import Base
from relational_database.relational_database import Session
from typing import Any, Callable, Iterable

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
    def add_element(self, Table: Base, args: Iterable):
        self.session.add(Table(*args))

    @commit_session
    def hello(self, name):
        print(f'hello {name}')