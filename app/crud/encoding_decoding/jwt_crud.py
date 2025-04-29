from datetime import datetime, timedelta
from fastapi import HTTPException, status
from ...schemas.encoding_decoding.jwt_schema import (
    JWTDecodeRequest,
    JWTDecodeResponse,
    JWTEncodeRequest,
    JWTEncodeResponse,
)
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError, JWTClaimsError

def encode_jwt_logic(data: JWTEncodeRequest) -> JWTEncodeResponse:
    try:
        payload = data.payload.copy()
        
        # Add expiry if specified
        expires_at = None
        if data.expiry_minutes:
            expires_at = datetime.now() + timedelta(minutes=data.expiry_minutes)
            payload["exp"] = int(expires_at.timestamp())
        
        # Add issued at timestamp
        payload["iat"] = int(datetime.now().timestamp())
        
        token = jwt.encode(
            claims=payload,  # Changed 'payload' to 'claims' for clarity and correctness
            key=data.secret,
            algorithm=data.algorithm,
            headers=data.headers
        )
        
        return JWTEncodeResponse(token=token, expires_at=expires_at)
    
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to encode JWT: {str(e)}"
        )

def decode_jwt_logic(data: JWTDecodeRequest) -> JWTDecodeResponse:
    try:
        # Decode token
        options = {"verify_exp": data.verify_expiry}
        decoded_payload = jwt.decode(
            token=data.token,  # Changed 'jwt' to 'token' for consistency
            key=data.secret,
            algorithms=[data.algorithm],
            options=options
        )
        
        decoded_header = jwt.get_unverified_header(data.token)
        
        # Extract timestamps
        issued_at = (
            datetime.fromtimestamp(decoded_payload.get("iat"))
            if decoded_payload.get("iat")
            else None
        )
        expires_at = (
            datetime.fromtimestamp(decoded_payload.get("exp"))
            if decoded_payload.get("exp")
            else None
        )
        
        return JWTDecodeResponse(
            payload=decoded_payload,
            headers=decoded_header,
            issued_at=issued_at,
            expires_at=expires_at
        )
    
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except JWTClaimsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid claims in token"
        )
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Token decoding failed: {str(e)}"
        )