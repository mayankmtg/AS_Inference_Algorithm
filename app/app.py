from models.database import Database
from models.models import get_declarative_base
from optparse import OptionParser
from sqlalchemy.orm import sessionmaker
import os
from populate.populate_BGPGraph import PopulateBGPGraph 


# Optional Arguments
parser = OptionParser()
parser.add_option("-c", "--create_tables",
                    dest="create_tables",
                    help="True: create tables in db; or False",
                    default="False")
parser.add_option("-p", "--populate_tables",
                    dest="populate_tables",
                    help="True: Populate tables using data/ directory",
                    default="False")

(options, args) = parser.parse_args()

# Variables
DB = Database()
Session = sessionmaker(DB)
Session.configure(bind = DB.db_engine)
session = Session()
# Create Tables
if options.create_tables == "True":
    base = get_declarative_base()
    DB.create_all(base)


# Populate Tables
if options.populate_tables == "True":
    PopulateBGPGraph(os.path.abspath('data/'), session).populate_all_bgp_files()