from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.models.base import engine
from src.main import app


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
        # statement = delete(Item)
        # session.execute(statement)
        # statement = delete(User)
        # session.execute(statement)
        # session.commit()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c
