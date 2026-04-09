from fastapi import Depends, HTTPException, status
from utils.auth_dependency import verify_token


def require_roles(allowed_roles: list):

    def role_checker(user=Depends(verify_token)):

        if user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission"
            )

        return user

    return role_checker