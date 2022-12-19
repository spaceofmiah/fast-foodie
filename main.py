from fastapi import FastAPI

from routers.foods import router as food_router
from routers.users import router as user_router
from routers.auth import router as auth_router



app = FastAPI(
    title="FastFoodie",
    contact={
        "name": "spaceofmiah",
        "email": "spaceofmiah@gmail.com",
        "url": "https://spaceofmiah.github.io",
    },
    description="Learning fastapi using a demo food api standard",
    terms_of_service="https://github.com/spaceofmiah/fast-foodie",
)
app.include_router(food_router)
app.include_router(user_router)
app.include_router(auth_router)



