from dotenv import load_dotenv
import os
load_dotenv()
print('Host:', os.getenv('MYSQL_HOST'))
print('Port:', os.getenv('MYSQL_PORT'))  
print('Database:', os.getenv('MYSQL_NAME'))
