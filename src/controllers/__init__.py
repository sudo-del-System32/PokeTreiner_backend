from jose import jwt, ExpiredSignatureError, JOSEError, JWTError
from typing import Any, Annotated
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src import SECRET_KEY, ALGORITHM_TO_HASH
from src.services.userService import UserService


def get_current_user(token: str):
    
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM_TO_HASH)
        user_id = payload.get("id")

        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user is not authorized")

        user = UserService().read_user_by_id({"user_id": user_id})

        # Ja feito na funçao user id
        # if not user:
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

        return user.model_dump(exclude_unset=True)

    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="expired token")
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid token")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Error in user authorization")

user_dependency = Annotated[dict[str, Any], Depends(get_current_user)]
