from dotenv import load_dotenv

load_dotenv()

from app import create_app, create_tables

app = create_app()

if __name__ == "__main__":
    create_tables()
    app.run(host="0.0.0.0", debug=True)
