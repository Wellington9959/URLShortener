from app.config import settings
from app.routes import router
from app.setup import create_application

app = create_application(router=router, settings=settings)
