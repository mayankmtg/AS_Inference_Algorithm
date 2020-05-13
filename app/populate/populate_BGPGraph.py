from glob import glob
from models.models import IPPrefix, BaseAS, BGPGaph
from populate.populate_IPPrefix import PopulateIPPrefix
from populate.populate_BaseAS import PopulateBaseAS
from typing import List

class PopulateBGPGraph:
    """
    Class for populating database tables
    """
    def __init__(self, data_dir: str, session):
        self.data_dir = data_dir
        self.session = session
    
    def populate_all_bgp_files(self) -> None:
        """
        Function to iterate through all the .rib files and populate each

        Returns:
            None
        """
        for bgp_rib_file in glob(self.data_dir + '/*.rib'):
            print ("reading: ", bgp_rib_file)
            self.populate_bgp_file(bgp_rib_file)
    
    def populate_bgp_file(self, bgp_rib_file_name: str) -> None:
        """
        Method to populate the bgp_rib_file
        
        Args:
            bgp_rib_file_name (str): filename containing all the bgp advertisements
        
        Returns:
            None
        """
        with open(bgp_rib_file_name) as bgp_rib_file:
            for bgp_advertisement in bgp_rib_file:
                self.populate_bgp_advertisement(bgp_advertisement)
    
    def populate_bgp_advertisement(self, bgp_advertisement: str) -> None:
        """
        Method to populate each bgp_advertisement of the file

        Args:
            bgp_advertisement (str): bgp_advertisement captured by routeviews
        
        Returns:
            None
        """
        bgp_advertisement_list = bgp_advertisement.split()
        # populate the found ip prefix
        ip_prefix = bgp_advertisement_list[0]
        ip_prefix_id = PopulateIPPrefix(ip_prefix, self.session).get_IPPrefix(ip_prefix).id
        
        # extract path and perform cleaning
        path_list = bgp_advertisement_list[1:]
        clean_path_list = self.clean_path(path_list)
        
        # populate base ASes found in this path
        PopulateBaseAS(ip_prefix_id, clean_path_list, self.session)

        # populate BGP graph
        self.populate_bgp_graph(ip_prefix_id, '|'.join(clean_path_list))

    def clean_path(self, path_list: List[str]) -> None:
        """
        Method to clean captured bgp path
        
        Args:
            path_list (List): path list in the order found in ribs
        
        Returns:
            None
        """
        clean_path = [path_list[0]]
        for ind in range(1, len(path_list)):
            if path_list[ind-1] != path_list[ind]:
                clean_path.append(path_list[ind])
        clean_path.reverse()
        return clean_path

    def populate_bgp_graph(self, prefix_id: int, path: str) -> None:
        """
        Method definition to populate bgp_graph table

        Args:
            prefix_id (int): prefix_id for the BGPGraph row population
            path (str): formatted path with ASes separated by '|'
        
        Returns:
            None
        """
        if not self.session.query(BGPGaph).filter_by(prefix_id=prefix_id, path=path).first():
            self.session.add(BGPGaph(prefix_id=prefix_id, path=path))
        self.session.commit()