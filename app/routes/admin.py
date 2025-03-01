from math import ceil
from typing import List, Dict

from fastapi import APIRouter, Request, status, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.schemas.product import NewData, NewProduct, PrdAttach, RowData
from app.services.product import ProductService
from app.services.user import UserService

admin_router = APIRouter()

# jinja2 설정
templates = Jinja2Templates(directory='views/templates')
admin_router.mount('/static', StaticFiles(directory='views/static'), name='static')


@admin_router.get('/', response_class=HTMLResponse)
def admin(req: Request):
    return templates.TemplateResponse('admin/admin.html', {'request': req})


@admin_router.get('/mgproduct/{cpg}', response_class=HTMLResponse)
def mgproduct(req: Request, cpg: int):
    stpg = int((cpg - 1) / 10) * 10 + 1
    pdlist, cnt = ProductService.select_product(cpg)
    allpage = ceil(cnt / 10)
    return templates.TemplateResponse('admin/mgproduct.html', {'request': req, 'pdlist':pdlist,
        'cpg': cpg, 'stpg': stpg, 'allpage': allpage, 'baseurl': '/admin/mgproduct/'})


@admin_router.get('/mgproduct/{category}/{search}/{cpg}', response_class=HTMLResponse)
def mgproduct_find(req: Request, category: str, search: str, cpg: int):
    stpg = int((cpg - 1) / 10) * 10 + 1
    pdlist, cnt = ProductService.find_select_product(category, '%' + search + '%', cpg)
    allpage = ceil(cnt / 10)
    return templates.TemplateResponse('admin/mgproduct.html',
        {'request': req, 'pdlist': pdlist,'cpg': cpg, 'stpg': stpg, 'allpage': allpage, 'baseurl': f'/admin/mgproduct/{category}/{search}/'})


@admin_router.post('/mgproduct1')
def mgproductok(rows_data: Dict[int, RowData]):
    result = ProductService.update_product(rows_data)
    res_url = '/error'
    if result.rowcount > 0: res_url = '/admin/mgproduct/1'
    return RedirectResponse(res_url, status_code=status.HTTP_302_FOUND)


@admin_router.post('/mgproduct2')
def deleteprd(del_data: Dict[str, List[int]]):
    result = ProductService.delete_product(del_data)
    res_url = '/error'
    if result.rowcount > 0: res_url = '/admin/mgproduct/1'
    return RedirectResponse(res_url, status_code=status.HTTP_302_FOUND)


@admin_router.get('/rgproduct', response_class=HTMLResponse)
def rgproduct(req: Request):
    return templates.TemplateResponse('admin/rgproduct.html', {'request': req})


@admin_router.post('/rgproduct')
def rgproductok(dto: NewData):
    pdto = NewProduct(prdname=dto.prdname, category=dto.category, stack=dto.stack, price=dto.price, contents=dto.contents)
    result = ProductService.insert_product(pdto)
    padto = PrdAttach(prdno=result.inserted_primary_key[0], img1=dto.img1, img2=dto.img2, img3=dto.img3, img4=dto.img4)
    result = ProductService.insert_prdattach(padto)

    res_url = '/error'
    if result.rowcount > 0: res_url = '/admin/mgproduct/1'
    return RedirectResponse(res_url, status_code=status.HTTP_302_FOUND)


@admin_router.post('/upload')
async def upload(images: List[UploadFile] = File()):
    list = await ProductService.process_upload(images)
    return {"message":"이미지업로드 성공", "filename" : list}


@admin_router.get('/mguser/{cpg}', response_class=HTMLResponse)
def mguser(req: Request, cpg: int):
    stpg = int((cpg - 1) / 10) * 10 + 1
    udlist, cnt = UserService.select_user(cpg)
    allpage = ceil(cnt / 10)
    return templates.TemplateResponse('admin/mguser.html',
          {'request': req, 'udlist': udlist, 'cpg': cpg, 'stpg': stpg, 'allpage': allpage, 'baseurl': '/admin/mguser/'})


@admin_router.get('/mguser/{ftype}/{fkey}/{cpg}', response_class=HTMLResponse)
def rgproduct_find(req: Request, ftype: str, fkey: str, cpg: int):
    stpg = int((cpg - 1) / 10) * 10 + 1
    udlist, cnt = UserService.search_select_user(ftype, '%' + fkey + '%', cpg)
    allpage = ceil(cnt / 15)
    return templates.TemplateResponse('admin/mguser.html',
          {'request': req, 'udlist': udlist, 'cpg': cpg, 'stpg': stpg, 'allpage': allpage, 'baseurl': f'/admin/mguser/{ftype}/{fkey}/'})


@admin_router.post('/mguser1', response_class=HTMLResponse)
def autoritychange(acdto: Dict[str, str]):
    result = UserService.update_user(acdto)
    res_url = '/error'
    if result.rowcount > 0: res_url = '/admin/mguser'
    return RedirectResponse(res_url, status_code=status.HTTP_302_FOUND)


@admin_router.post('/mguser2', response_class=HTMLResponse)
def deleteuser(dudto : Dict[str, List[int]]):
    result = UserService.delete_user(dudto)
    res_url = '/error'
    if result.rowcount > 0: res_url = '/admin/mguser'
    return RedirectResponse(res_url, status_code=status.HTTP_302_FOUND)

