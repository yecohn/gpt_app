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

    # Create new database element
    @commit_session
    def add_element(self, Table: Base, args: Iterable):
        self.session.add(Table(*args))

    @commit_session
    def del_element(self, Table: Base, _id: int):
        to_delete = self.session.query(Table).filter_by(id=_id).first()
        self.session.delete(to_delete)

    def access_full_table(self, Table: Base):
        return self.session.query(Table).all()
    
    def access_element(self, Table: Base, _id: int):
        return self.session.query(Table).filter_by(id=_id).first()