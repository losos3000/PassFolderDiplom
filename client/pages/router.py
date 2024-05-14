from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from server.data.router import read_data_all

TEMPLATE_DIR = "./client/templates"


router = APIRouter()


templates = Jinja2Templates(directory=TEMPLATE_DIR)


@router.get("/")
def get_data_page(request: Request, data_records=Depends(read_data_all)):
    return templates.TemplateResponse("data.html", {"request": request, "data_records": data_records["data"]})
