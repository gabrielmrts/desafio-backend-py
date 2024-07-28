import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from app.main import app
from app.database.session import get_db
from app.database.base_class import Base
from app.core.config import settings
from sqlalchemy.orm import Session

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session
)

# Fixture para o Banco de Dados de Teste
@pytest.fixture(scope="module", autouse=True)
def setup_db():
    # Criar todas as tabelas
    Base.metadata.create_all(bind=engine)
    yield
    # Dropar todas as tabelas
    Base.metadata.drop_all(bind=engine)

# Fixture para sobrescrever a dependência de banco de dados
@pytest.fixture(scope="module")
def db_session_override():
    def _override_get_db():
        with TestingSessionLocal() as session:
            yield session
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides[get_db] = get_db

# Configuração do Cache
@pytest.fixture(scope="module", autouse=True)
def setup_cache():
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
