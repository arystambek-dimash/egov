from app.utils import import_routers
from fastapi import APIRouter

router = APIRouter()
import_routers(__name__)
