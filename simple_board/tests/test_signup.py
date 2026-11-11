import unittest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from main import app
from repository.database import Base, get_db
from repository.models.user import User
from core.security import verify_password


class SignupTest(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(self.engine)

        def test_db():
            with Session(self.engine) as db:
                yield db

        app.dependency_overrides[get_db] = test_db
        self.client = TestClient(app)

    def tearDown(self):
        self.client.close()
        app.dependency_overrides.clear()
        self.engine.dispose()

    def test_signup_hashes_password_and_rejects_duplicate_email(self):
        payload = {
            "email": "member@example.com",
            "password": "Example1!",
            "name": "회원",
        }
        response = self.client.post("/auth", json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "회원가입이 완료되었습니다.")

        with Session(self.engine) as db:
            user = db.scalar(select(User).where(User.email == payload["email"]))
            self.assertEqual(response.json()["user_id"], user.user_id)
            self.assertNotEqual(user.password, payload["password"])
            self.assertTrue(verify_password(payload["password"], user.password))

        duplicate = self.client.post("/auth", json=payload)
        self.assertEqual(duplicate.status_code, 409)

    def test_signup_rejects_weak_password(self):
        response = self.client.post(
            "/auth",
            json={"email": "member@example.com", "password": "weak", "name": "회원"},
        )
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
