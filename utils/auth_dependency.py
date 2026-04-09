from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timezone

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

security = HTTPBearer()

def verify_token(credentials=Depends(security)):

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": False}   # 🚨 disable auto check
        )

        exp = payload.get("exp")

        # ✅ Manual expiry check (FIX)
        now = datetime.now(timezone.utc).timestamp()

        print("NOW:", now)
        print("EXP:", exp)

        if exp is None or now > exp:
            raise HTTPException(status_code=401, detail="Token expired")

        return {
            "user_id": payload.get("user_id"),
            "role": payload.get("role")
        }

    except JWTError as e:
        print("JWT ERROR:", str(e))
        raise HTTPException(status_code=401, detail="Invalid token")