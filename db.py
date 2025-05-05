from sqlmodel import create_engine, SQLModel, Session

DATABASE = "sqlite:///db.sqlite"
engine = create_engine(DATABASE)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
