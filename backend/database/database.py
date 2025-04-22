import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv() # Ładuje zmienne z pliku .env

# Odczytaj dane konfiguracyjne bazy danych ze zmiennych środowiskowych
DB_USER = os.getenv("MYSQL_USER", "user")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")
DB_HOST = os.getenv("MYSQL_HOST", "localhost")
DB_PORT = os.getenv("MYSQL_PORT", "3306")
DB_NAME = os.getenv("MYSQL_DATABASE", "empathy_game_db")

# Format: "mysql+mysqlconnector://user:password@host:port/database_name"
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# Alternatywnie dla pymysql: f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# Silnik SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # pool_recycle=3600 # Opcjonalnie, do odświeżania połączeń
)

# Fabryka sesji
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Klasa bazowa dla modeli ORM
Base = declarative_base()

# Zależność FastAPI do uzyskiwania sesji bazy danych w endpointach
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Funkcja do inicjalizacji bazy danych (tworzenia tabel)
# Można ją wywołać raz przy starcie aplikacji lub użyć narzędzi migracyjnych jak Alembic
def init_db():
    Base.metadata.create_all(bind=engine)