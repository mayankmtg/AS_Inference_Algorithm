from sqlalchemy import create_engine

class Database():
    """
    Class to initialise connection object
    """
    
    # Use user, password, hostname and databasename according to config
    #  TODO:: fetch this information from some config
    def __init__(self):
        self.db_engine = create_engine('postgresql://{}:{}@{}/{}'.format('mayank', 'mayank', 'localhost', 'knownpath'))
        print ("database engine initialised")
    
    def create_all(self, base):
        base.metadata.create_all(self.db_engine)
        print ("models created")