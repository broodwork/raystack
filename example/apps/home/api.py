from fastapi import APIRouter


router = APIRouter()


# Include your routes here.

# Example:
@router.get("/example_api")
def example():
    return {"message": "text"}