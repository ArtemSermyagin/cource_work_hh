import os
from dotenv import load_dotenv

load_dotenv()

employers_id = [
    36227, 3643187, 5912899, 10035323, 10158780, 4429980, 4717703, 5064090, 54794, 4775363
]

host = "localhost"
database = "hh"
user = "postgres"
password = os.environ.get("PASSWORD")

