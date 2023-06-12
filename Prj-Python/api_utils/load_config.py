
from pydantic import BaseSettings
import os

curr_path = os.path.dirname(os.path.abspath(__file__))
proj_path = os.path.dirname(os.path.dirname(curr_path))
# print("curr_path:", curr_path)
# print("proj_path:", proj_path)


class MyConfig(BaseSettings):
    # api端口
    port = 8018
    # modelPath = os.path.join(proj_path, "models")   # 模型路径
    # model_name = os.path.join(modelPath, 'an_model.pkl')   # 模型名称
    device = '0'
    augment = False
    agnostic_nms = False

    #环境变量设置
    class Config:
        fields = {
            # 'helloPrefix': {'env': 'helloPrefix'.upper()},
            'modelPath':{'env': 'modelPath'.upper()},
            # 'ocr_url': {'env': 'ocr_url'.upper()},
            'device': {'env': 'device'.upper()}
        }


cfg = MyConfig()
