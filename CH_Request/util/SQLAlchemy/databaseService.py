from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import scoped_session


class DatabaseService:
    def __init__(self, host, port, username, password, database):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database

        # echo for debug
        self.engine = create_engine("mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8"
                                    % (self.username, self.password, self.host, self.port, self.database),
                                    echo=False, poolclass=NullPool)

        Session = sessionmaker(bind=self.engine)

        self.session = Session()

    def close_engine(self):
        self.session.close()
        self.session.bind.dispose()
        self.engine.dispose()
