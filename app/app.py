import os
from flask import Flask

app = Flask(__name__)

ENVIRONMENT = os.getenv("ENVIRONMENT", "DEV")
APPLICATION = os.getenv("APPLICATION", "customer-app")
PORT = int(os.getenv("PORT", "8080"))
NETWORK = os.getenv("NETWORK", "")
DATABASE = os.getenv("DATABASE", "")


@app.route("/")
def home():
    return {
        "application": APPLICATION,
        "environment": ENVIRONMENT,
        "port": PORT,
        "network": NETWORK,
        "database": DATABASE
    }


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080
    )
