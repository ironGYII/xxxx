FROM python:latest

# 设置工作目录
WORKDIR /app


# 安装依赖库
# RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --no-cache-dir web3==6.8.0 -i https://pypi.tuna.tsinghua.edu.cn/simple
ENV PYTHONPATH "${PYTHONPATH}:."

# 拷贝应用程序代码到容器中
COPY . /app