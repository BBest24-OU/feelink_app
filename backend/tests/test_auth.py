"""
Unit tests for authentication (JWT, password hashing)
"""
import pytest
from datetime import datetime, timedelta
from jose import JWTError

from app.security.password import hash_password, verify_password
from app.security.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_token,
    SECRET_KEY,
    ALGORITHM
)


class TestPasswordHashing:
    """Tests for password hashing utilities"""

    def test_hash_password_creates_hash(self):
        """Test that hash_password creates a hash different from plaintext"""
        password = "mysecurepassword123"
        hashed = hash_password(password)

        assert hashed != password
        assert len(hashed) > 0
        assert hashed.startswith("$2b$")  # bcrypt prefix

    def test_hash_password_different_hashes(self):
        """Test that same password generates different hashes (salt)"""
        password = "mysecurepassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)

        # Due to random salt, hashes should be different
        assert hash1 != hash2

    def test_verify_password_correct(self):
        """Test verify_password with correct password"""
        password = "mysecurepassword123"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test verify_password with incorrect password"""
        password = "mysecurepassword123"
        wrong_password = "wrongpassword"
        hashed = hash_password(password)

        assert verify_password(wrong_password, hashed) is False

    def test_verify_password_empty(self):
        """Test verify_password with empty password"""
        password = "mysecurepassword123"
        hashed = hash_password(password)

        assert verify_password("", hashed) is False

    def test_hash_password_special_characters(self):
        """Test password hashing with special characters"""
        password = "P@ssw0rd!#$%^&*()"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_hash_password_unicode(self):
        """Test password hashing with unicode characters"""
        password = "пароль123"  # Russian
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True


class TestJWTTokens:
    """Tests for JWT token generation and validation"""

    def test_create_access_token_basic(self):
        """Test creating a basic access token"""
        data = {"sub": "test@example.com", "user_id": 1}
        token = create_access_token(data)

        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_custom_expiry(self):
        """Test creating access token with custom expiration"""
        data = {"sub": "test@example.com"}
        expires_delta = timedelta(minutes=30)
        token = create_access_token(data, expires_delta)

        payload = decode_token(token)
        exp = datetime.fromtimestamp(payload["exp"])
        now = datetime.utcnow()

        # Should expire in approximately 30 minutes
        diff = (exp - now).total_seconds() / 60
        assert 29 <= diff <= 31

    def test_create_refresh_token(self):
        """Test creating a refresh token"""
        data = {"sub": "test@example.com", "user_id": 1}
        token = create_refresh_token(data)

        assert isinstance(token, str)
        assert len(token) > 0

        payload = decode_token(token)
        assert payload["type"] == "refresh"

    def test_decode_token_valid(self):
        """Test decoding a valid token"""
        data = {"sub": "test@example.com", "user_id": 1}
        token = create_access_token(data)

        payload = decode_token(token)

        assert payload["sub"] == "test@example.com"
        assert payload["user_id"] == 1
        assert payload["type"] == "access"
        assert "exp" in payload

    def test_decode_token_invalid(self):
        """Test decoding an invalid token"""
        invalid_token = "invalid.token.here"

        with pytest.raises(JWTError):
            decode_token(invalid_token)

    def test_decode_token_expired(self):
        """Test decoding an expired token"""
        data = {"sub": "test@example.com"}
        # Create token that expired 1 hour ago
        expires_delta = timedelta(hours=-1)
        token = create_access_token(data, expires_delta)

        with pytest.raises(JWTError):
            decode_token(token)

    def test_verify_token_valid_access(self):
        """Test verifying a valid access token"""
        data = {"sub": "test@example.com", "user_id": 1}
        token = create_access_token(data)

        payload = verify_token(token, token_type="access")

        assert payload is not None
        assert payload["sub"] == "test@example.com"
        assert payload["type"] == "access"

    def test_verify_token_valid_refresh(self):
        """Test verifying a valid refresh token"""
        data = {"sub": "test@example.com", "user_id": 1}
        token = create_refresh_token(data)

        payload = verify_token(token, token_type="refresh")

        assert payload is not None
        assert payload["sub"] == "test@example.com"
        assert payload["type"] == "refresh"

    def test_verify_token_wrong_type(self):
        """Test verifying token with wrong type"""
        data = {"sub": "test@example.com"}
        access_token = create_access_token(data)

        # Try to verify as refresh token
        payload = verify_token(access_token, token_type="refresh")

        assert payload is None

    def test_verify_token_invalid(self):
        """Test verifying an invalid token"""
        invalid_token = "invalid.token.here"

        payload = verify_token(invalid_token, token_type="access")

        assert payload is None

    def test_verify_token_expired(self):
        """Test verifying an expired token"""
        data = {"sub": "test@example.com"}
        expires_delta = timedelta(hours=-1)
        token = create_access_token(data, expires_delta)

        payload = verify_token(token, token_type="access")

        assert payload is None

    def test_token_contains_expiration(self):
        """Test that tokens contain expiration field"""
        data = {"sub": "test@example.com"}
        token = create_access_token(data)

        payload = decode_token(token)

        assert "exp" in payload
        assert isinstance(payload["exp"], (int, float))

    def test_token_preserves_custom_data(self):
        """Test that tokens preserve custom data fields"""
        data = {
            "sub": "test@example.com",
            "user_id": 42,
            "roles": ["user", "admin"],
            "custom_field": "custom_value"
        }
        token = create_access_token(data)

        payload = decode_token(token)

        assert payload["sub"] == "test@example.com"
        assert payload["user_id"] == 42
        assert payload["roles"] == ["user", "admin"]
        assert payload["custom_field"] == "custom_value"

    def test_access_token_has_correct_type(self):
        """Test that access tokens have correct type field"""
        data = {"sub": "test@example.com"}
        token = create_access_token(data)

        payload = decode_token(token)

        assert payload["type"] == "access"

    def test_refresh_token_has_correct_type(self):
        """Test that refresh tokens have correct type field"""
        data = {"sub": "test@example.com"}
        token = create_refresh_token(data)

        payload = decode_token(token)

        assert payload["type"] == "refresh"

    def test_token_different_for_different_data(self):
        """Test that different data produces different tokens"""
        data1 = {"sub": "user1@example.com"}
        data2 = {"sub": "user2@example.com"}

        token1 = create_access_token(data1)
        token2 = create_access_token(data2)

        assert token1 != token2

    def test_token_uses_correct_algorithm(self):
        """Test that tokens use the correct algorithm"""
        from jose import jwt

        data = {"sub": "test@example.com"}
        token = create_access_token(data)

        # Decode without verification to check algorithm
        unverified = jwt.get_unverified_header(token)

        assert unverified["alg"] == ALGORITHM


class TestAuthenticationIntegration:
    """Integration tests for authentication flow"""

    def test_full_auth_flow(self):
        """Test complete authentication flow: register -> login -> verify"""
        # 1. Hash password (registration)
        password = "userpassword123"
        password_hash = hash_password(password)

        # 2. Verify password (login)
        is_valid = verify_password(password, password_hash)
        assert is_valid is True

        # 3. Create access token (login response)
        user_data = {"sub": "user@example.com", "user_id": 1}
        access_token = create_access_token(user_data)

        # 4. Verify token (on subsequent requests)
        payload = verify_token(access_token, token_type="access")
        assert payload is not None
        assert payload["sub"] == "user@example.com"
        assert payload["user_id"] == 1

    def test_wrong_password_flow(self):
        """Test authentication flow with wrong password"""
        # 1. Hash password
        password = "correctpassword"
        password_hash = hash_password(password)

        # 2. Try to verify with wrong password
        wrong_password = "wrongpassword"
        is_valid = verify_password(wrong_password, password_hash)

        # Should fail verification
        assert is_valid is False

    def test_token_refresh_flow(self):
        """Test token refresh flow"""
        # 1. Create initial tokens
        user_data = {"sub": "user@example.com", "user_id": 1}
        access_token = create_access_token(user_data)
        refresh_token = create_refresh_token(user_data)

        # 2. Verify refresh token
        refresh_payload = verify_token(refresh_token, token_type="refresh")
        assert refresh_payload is not None

        # 3. Create new access token from refresh
        new_access_token = create_access_token(user_data)

        # 4. Both access tokens should work
        payload1 = verify_token(access_token, token_type="access")
        payload2 = verify_token(new_access_token, token_type="access")

        assert payload1 is not None
        assert payload2 is not None
        assert payload1["sub"] == payload2["sub"]
