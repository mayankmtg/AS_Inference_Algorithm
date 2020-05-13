from models.models import IPPrefix

class PopulateIPPrefix:
    """
    Class for populating IPPrefix model 
    """
    def __init__(self, ip_prefix: str, session):
        """
        Initialisation method

        Args:
            ip_prefix (str): The value of ip_prefix to be populated
            session: the sqlalchemy session variable to transactions in db
        """
        self.session = session
        self.ip_prefix = ip_prefix
        if not self.get_IPPrefix(ip_prefix):
            ipPrefix = IPPrefix(prefix = ip_prefix)
            self.session.add(ipPrefix)

    def get_IPPrefix(self, ip_prefix: str) -> IPPrefix:
        """
        Method to get the IPPrefix type object from ip_prefix string
        
        Args:
            ip_prefix (str): The ip_prefix string
        
        Returns:
            IPPrefix: Corresponding object
        """
        return self.session.query(IPPrefix).filter_by(prefix = ip_prefix).first()