from dotenv import load_dotenv

load_dotenv()

import os  # noqa: E402

from app import create_app  # noqa: E402

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("FLASK_PORT", 5500)), debug=True)
