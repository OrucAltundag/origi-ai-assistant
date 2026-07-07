from fastapi import HTTPException, status


def require_confirmation(confirm: bool) -> None:
    if not confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This action is sensitive. Resend the request with confirm=true.",
        )
