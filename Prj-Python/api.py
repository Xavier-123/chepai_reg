# -*- coding: utf-8 -*-

"""
Created 2023/06/7
@author: Xiaoaowen
describe: service
"""

from pydantic import BaseModel, Field
from typing import Any
from fastapi import FastAPI, Request, status, Query
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn
import math

from api_utils.log import logger
from api_utils.result import result, Code
from api_utils.load_config import cfg
from inference import infer
from sql import *
import time

app = FastAPI()


# 参数有效性检查，重定义返回结构，必要，无需修改
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    res = result(False, exc.errors(), None, Code.InvalidParameter)
    logger.error(res.__dict__)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=res.__dict__,
    )


# 返回值结构及样例定义
class Response(BaseModel):
    isSuc: bool = Field(..., example=True)
    code: int = Field(..., example=0)
    msg: str = Field(..., example="success")
    res: Any = Field(..., example="hello, <text>")


class Request(BaseModel):
    # 必要参数
    image_base64str: str = Query(..., description="图片Base64str编码")


'''进停车场'''
# @app.post("/enter_park", response_model=Response, tags=["进停车场"])
@app.post("/enter_park", tags=["进停车场"])
def enter_park(Data: Request):
    logger.info("---------- Inference start ---------")
    try:
        image_base64str = Data.image_base64str
        _res, code = infer(image_base64str)
        _res = _res[0]
        if len(_res) > 1:
            _res = _res[0]
        t_start = time.time()

        car_type = None
        # assert len(_res) == 1, logger.info("识别出多个车牌号！")

        '''存入sql'''
        if select_car(_res):
            return result(False, "车牌号已存在！", None, -1).__dict__
        else:
            is_success, save_info = save_car_info(_res, car_type, t_start)
        res = [_res]

        if is_success:
            content = {"isSuc": True, "code": code, "msg": "欢迎光临！", "data": str(res)}
        else:
            content = {"isSuc": True, "code": code, "msg": save_info, "data": str(res)}
        logger.info("---------- Inference stop ---------")
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except:
        return result(False, "decode str error", None, -1).__dict__


'''出停车场'''
@app.post("/out_park", response_model=Response, tags=["出停车场"])
def out_park(Data: Request):
    logger.info("---------- start ---------")
    try:
        image_base64str = Data.image_base64str
        _res, code = infer(image_base64str)
        _res = _res[0]
        if len(_res) > 1:
            _res = _res[0]
        t_end = time.time()

        '''读取sql'''
        data = select_car(_res)
        car_time = data[-1]
        if data is not None:
            t_start = datetime.timestamp(car_time)
            t_min = math.ceil((t_end - t_start) / 60)
            del_car(_res)
        else:
            return result(False, "该车辆未驶入！", None, -1).__dict__

        res = [_res, t_min]
        content = {"isSuc": True, "code": code, "msg": f"祝你旅途愉快！", "data": str(res)}
        logger.info(content)
        logger.info("---------- end ---------")
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)
    except:
        return result(False, "decode str error", None, -1).__dict__


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=18000, log_config=None, access_log=False)
