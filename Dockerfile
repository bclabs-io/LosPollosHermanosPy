# 第一階段：建構環境與安裝 Poetry 相依套件
FROM python:3.12-slim AS builder

# 安裝系統相依套件（Poetry 需要 curl 等工具）
RUN apt update && apt install -y curl build-essential

# 安裝 Poetry 並設定環境變數
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app
COPY pyproject.toml poetry.lock ./

# 使用 Poetry 安裝相依套件
# 變更設定：不建立虛擬環境，因為 Docker 本身就是隔離環境
RUN poetry config virtualenvs.create false \
    # 只安裝 main 的套件，即不含 dev、test 等 group
    && poetry install --only main --no-root --no-interaction --no-ansi

# 第二階段：建立乾淨的 image
FROM python:3.12-slim

WORKDIR /app

# 複製專案程式
# 從 builder 階段複製已安裝的 site-packages
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . .

# 執行資料庫遷移
RUN python migrate.py

# 啟動 Flask 應用程式
EXPOSE 5500
CMD [ "python", "main.py" ]
