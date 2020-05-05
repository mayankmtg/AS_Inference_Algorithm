from models.database import Database
from models.models import get_declarative_base
from optparse import OptionParser


# Optional Arguments
parser = OptionParser()
parser.add_option("-c", "--create_tables",
                    dest="create_tables",
                    help="True: create tables in db; or False",
                    default="False")

(options, args) = parser.parse_args()

# Create Tables
if options.create_tables == "True":
    DB = Database()
    base = get_declarative_base()
    DB.create_all(base)

