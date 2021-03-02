import base64
import glob
import os

# 需要导入到 EXE 的图片地址
import_pictures = glob.glob(r'./resource/*')

# 导出途径
target_path = r'./resource.py'

# 删除旧的文件
if os.path.exists(target_path):
    os.remove(target_path)

# 以追加的形式将通过 base64 转换后图片信息存储导出的文件中
with open(target_path,"a+") as f:
    for file_path in import_pictures:
        # 以 文件名称_文件类型 作为二进制信息的对象名
        file_name = (os.path.split(file_path)[-1]).replace('.', '_')
        with open(file_path,"rb") as pic:
            b64str = base64.b64encode(pic.read())
            write_data = f'{file_name} = {b64str}'
            f.write(write_data)
            f.write('\n')
