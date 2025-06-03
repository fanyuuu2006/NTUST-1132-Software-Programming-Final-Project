from dotenv import load_dotenv
load_dotenv(".env.local")
from api.webhook import app

app.run()