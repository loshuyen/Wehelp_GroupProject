from fastapi import *
from fastapi.responses import *
from fastapi.staticfiles import StaticFiles
from routers import weather, warning, discord

app = FastAPI()

app.include_router(weather.router)
app.include_router(warning.router)
app.include_router(discord.router)

app.mount("/css", StaticFiles(directory="../public/css"), name="css")
app.mount("/images", StaticFiles(directory="../public/images"), name="images")
app.mount("/view", StaticFiles(directory="view"), name="view")

@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("../static/index.html", media_type="text/html")

@app.get("/warning", include_in_schema=False)
async def index(request: Request):
	return FileResponse("../static/warning.html", media_type="text/html")

@app.get("/{county}", include_in_schema=False)
async def index(request: Request):
	return FileResponse("../static/county.html", media_type="text/html")


