from flask import Flask
import config

# bot = "botlib.Bot(creds, config)"
app = Flask(__name__)

async def hello_world():
    return "<p>Hello, World!</p>"

def api_start(bot_obj):
    global bot

    bot = bot_obj
    
    app.add_url_rule('/hello',  view_func=hello_world)

    app.run( 
        host=config.SERVICE_HOST, 
        port=config.SERVICE_PORT
    )