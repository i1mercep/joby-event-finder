from fastapi import APIRouter, FastAPI

from src.config import get_settings
from src.utils import load_routers

settings = get_settings()
is_debug = settings.log_level.lower() == "debug"
main_router = APIRouter(prefix=settings.api_prefix)

routers = load_routers(endpoints_path="src/endpoints")
for router_name, router in routers.items():
    main_router.include_router(router, tags=[router_name])

app = FastAPI(title=settings.app_name, debug=is_debug)
app.include_router(main_router)
