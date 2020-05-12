from glob import glob
from models.models import IPPrefix, BaseAS, BGPGaph

class PopulateIPPrefix:

    def __init__(self, ip_prefix: str, session):
        print ('adding prefix: ', ip_prefix)
        self.session = session
        self.ip_prefix = ip_prefix
        if not self.get_IPPrefix(ip_prefix):
            ipPrefix = IPPrefix(prefix = ip_prefix)
            self.session.add(ipPrefix)

    def get_IPPrefix(self, ip_prefix: str):
        return self.session.query(IPPrefix).filter_by(prefix = ip_prefix).first()

class PopulateBaseAS:

    def __init__(self, prefix_id: int, asns, session):
        self.session = session
        self.prefix_id = prefix_id
        self.asns = asns
        self.populate_base_as()

    def populate_base_as(self):
        new_asns = []
        
        for asn in self.asns:
            if not self.session.query(BaseAS).filter_by(prefix_id = self.prefix_id, asn = asn).first():
                new_asns.append(asn)
        
        for asn in new_asns:
            self.session.add(BaseAS(prefix_id=self.prefix_id, asn=asn))

class PopulateBGPGraph:
    """
    Class for populating database tables
    """
    def __init__(self, data_dir: str, session):
        self.data_dir = data_dir
        self.session = session
    
    def populate_all_bgp_files(self):
        """
        Function to iterate through all the .rib files and populate each
        """
        for bgp_rib_file in glob(self.data_dir + '/*.rib'):
            print ("reading: ", bgp_rib_file)
            self.populate_bgp_file(bgp_rib_file)
    
    def populate_bgp_file(self, bgp_rib_file_name: str):
        """
        Function to populate each bgp advertisement for the bgp_rib_file
        
        Args:
            bgp_rib_file (str): filename containing all the bgp advertisements
        """
        with open(bgp_rib_file_name) as bgp_rib_file:
            for bgp_advertisement in bgp_rib_file:
                self.populate_bgp_advertisement(bgp_advertisement)
    
    def populate_bgp_advertisement(self, bgp_advertisement):
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

    def clean_path(self, path_list):
        clean_path = [path_list[0]]
        for ind in range(1, len(path_list)):
            if path_list[ind-1] != path_list[ind]:
                clean_path.append(path_list[ind])
        clean_path.reverse()
        return clean_path

    def populate_bgp_graph(self, prefix_id: int, path: str):
        """
        Function definition to populate bgp_graph table
        """
        if not self.session.query(BGPGaph).filter_by(prefix_id=prefix_id, path=path).first():
            self.session.add(BGPGaph(prefix_id=prefix_id, path=path))
        self.session.commit()