from flask import Flask, jsonify
from threading import Thread
import logging
from configs import cfg

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    return 'TandavBots is running!'

@app.route('/status')
def status():
    return jsonify({
        "status": "online",
        "bot_name": cfg.BOT_NAME,
        "version": cfg.BOT_VERSION
    }), 200

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    logger.info("Starting Flask server...")
    try:
        run()
    except Exception as e:
        logger.error(f"Error starting Flask server: {e}")
