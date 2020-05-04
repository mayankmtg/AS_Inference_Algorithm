import sqlalchemy as db

class Database():
    """
    Class to initialise connection object
    """
    # Use user, password, hostname and databasename according to config
    #  TODO:: fetch this information from some config
    engine = db.create_engine('postgresql://{}:{}@{}/{}'.format('mayank', 'mayank', 'localhost', 'knownpath'))
    def __init__(self):
        self.connection = self.engine.connect()
