from enum import Enum
from pydantic import BaseModel

class HashAlgorithm(str, Enum):
    md5 = "md5"
    sha1 = "sha1"
    sha256 = "sha256"
    sha512 = "sha512"

class HashRequest(BaseModel):
    text: str
    algorithm: HashAlgorithm

class HashResponse(BaseModel):
    text: str
    algorithm: HashAlgorithm
    hashed_text: str