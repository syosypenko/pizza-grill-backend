from fastapi import APIRouter, Depends
from app.deps import require_role, get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/admin")
def admin_dashboard(user: User = Depends(require_role("admin"))):
    return {"msg": f"Hello Admin {user.username}"}

@router.get("/me")
def read_users_me(user: User = Depends(get_current_user)):
    return {"username": user.username, "role": user.role}
