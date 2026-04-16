from jose import jwt, ExpiredSignatureError, JWTError
from typing import Any, Annotated
from fastapi import HTTPException, status, Depends
from src import SECRET_KEY, ALGORITHM_TO_HASH
from src.services.userService import UserService

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated


form_auth_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
token_dependency = Annotated[str, Depends(oauth2_scheme)]

def get_current_user(token: token_dependency):
    
    try:
        payload = jwt.decode(
            token=token, 
            key=SECRET_KEY, 
            algorithms=ALGORITHM_TO_HASH
        )
        
        user_id = payload.get("id")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="user is not authorized"
            )

        user = UserService().get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="user not found"
            )

        return user

    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired token.")
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token.")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Error in user authorization.")

user_dependency = Annotated[dict[str, Any], Depends(get_current_user)]
