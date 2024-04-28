# 使用tiangolo/uvicorn-gunicorn-fastapi作為基礎映像
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

# 設置工作目錄
WORKDIR /app

# 將requirements.txt文件複製到容器中
COPY ./requirements.txt /requirements.txt

# 安裝依賴
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

# 將你的應用代碼複製到容器中
COPY ./app /app
