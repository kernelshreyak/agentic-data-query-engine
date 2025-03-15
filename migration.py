from sqlalchemy import create_engine
from data_models import *

import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL)

print(f"""Creating {len(Base.metadata.tables)} tables...""")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")