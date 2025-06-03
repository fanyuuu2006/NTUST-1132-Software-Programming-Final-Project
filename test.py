from dotenv import load_dotenv
load_dotenv(".env.local")
from api.reply_handler import reply_handler
print(reply_handler("我想要台積電的股價"))