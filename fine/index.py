from config import appconfig
from main import main

if __name__ == "__main__":
    main.app.run(debug=True, host=appconfig.HOST, port=appconfig.PORT)