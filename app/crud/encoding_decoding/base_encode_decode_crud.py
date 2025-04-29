import base64
import base58
from fastapi import HTTPException
from ...schemas.encoding_decoding.base_encode_decode_schema import BaseType

# Mapping for encoding functions
ENCODING_FUNCTIONS = {
    BaseType.base32: lambda text: base64.b32encode(text.encode()).decode(),
    BaseType.base58: lambda text: base58.b58encode(text.encode()).decode(),
    BaseType.base64: lambda text: base64.b64encode(text.encode()).decode(),
}

# Mapping for decoding functions
DECODING_FUNCTIONS = {
    BaseType.base32: lambda text: base64.b32decode(text.encode()).decode(),
    BaseType.base58: lambda text: base58.b58decode(text.encode()).decode(),
    BaseType.base64: lambda text: base64.b64decode(text.encode()).decode(),
}

def base_encode_logic(text: str, base_type: BaseType) -> dict:
    if not text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty")
    
    try:
        encoded_text = ENCODING_FUNCTIONS[base_type](text)
        return {
            "input_text": text,
            "base_type": base_type,
            "encoded_text": encoded_text
        }
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Invalid base type: {base_type}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Encoding failed: {str(e)}")

def base_decode_logic(encoded_text: str, base_type: BaseType) -> dict:
    if not encoded_text.strip():
        raise HTTPException(status_code=400, detail="Encoded text cannot be empty")
    
    try:
        decoded_text = DECODING_FUNCTIONS[base_type](encoded_text)
        return {
            "encoded_text": encoded_text,
            "base_type": base_type,
            "decoded_text": decoded_text
        }
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Invalid base type: {base_type}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Decoding failed: {str(e)}")