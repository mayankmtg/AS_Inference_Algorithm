from models.models import BaseAS
from typing import List

class PopulateBaseAS:
    """
    Class for populating BaseAS model
    """
    def __init__(self, prefix_id: int, asns: List[str], session):
        """
        Initialisation method

        Args:
            prefix_id (int): required prefix_id
            asns (List): List of all the asns
        
        Returns:
            None
        """
        self.session = session
        self.prefix_id = prefix_id
        self.asns = asns
        self.populate_base_as()

    def populate_base_as(self) -> None:
        """
        Method for actually populating BaseAS model

        Returns:
            None
        """
        new_asns = []
        
        for asn in self.asns:
            if not self.session.query(BaseAS).filter_by(prefix_id = self.prefix_id, asn = asn).first():
                new_asns.append(asn)
        
        for asn in new_asns:
            self.session.add(BaseAS(prefix_id=self.prefix_id, asn=asn))