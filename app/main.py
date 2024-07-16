from fastapi import *
from fastapi.responses import *
from routers import weather

app = FastAPI()

app.include_router(weather.router)

@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("../static/index.html", media_type="text/html")