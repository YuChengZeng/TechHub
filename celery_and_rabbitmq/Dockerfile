# 使用官方 Python 3.10 slim 映像作為基礎映像
FROM python:3.10-slim

# 設置工作目錄
WORKDIR /app

# 將requirements.txt文件複製到容器中
COPY ./requirements.txt /requirements.txt

# 安裝 Python 依賴
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

# 將當前目錄下的文件複製到容器中的 /app 目錄
COPY . /app

# 指定容器啟動時執行的命令（這裡需根據你的應用需求來指定，例如啟動 FastAPI 服務）
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
