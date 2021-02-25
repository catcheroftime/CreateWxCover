import base64

# 执行文件，将logo以文本的形式保存，方便打包

open_icon = open("icon.ico","rb")
b64str = base64.b64encode(open_icon.read())
open_icon.close()
write_data = "img = %s" % b64str
f = open("logo.py","w+")
f.write(write_data)
f.close()
