from sqlalchemy.engine import create_engine as create_mysql_engine



def create_engine(user, password, host, database):
    url = "mysql+pymysql://{}:{}@{}/{}".format(
        user, password, host, database
    )
    engine = create_mysql_engine(url, echo=True)
    return engine
