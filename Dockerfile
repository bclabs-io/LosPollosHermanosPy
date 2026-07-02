# ==========================================
# 第一階段：建構環境與安裝相依套件 (Builder)
# ==========================================
FROM python:3.12-slim AS builder

# 直接從官方映像檔複製 uv 執行檔，不需要裝 curl，更安全也更輕量
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 開啟預先編譯。讓 uv 在安裝套件時自動編譯成 bytecode (.pyc)，能加快第二階段容器的啟動速度
ENV UV_COMPILE_BYTECODE=1

WORKDIR /app

# 複製專案設定檔 (請先確保已將專案遷移至 uv，並產生 uv.lock)
COPY pyproject.toml uv.lock ./

# 使用 uv 同步套件，會預設建立專案目錄下的 `.venv`
# --frozen: 嚴格鎖定版本，不允許 uv 變更 lock 檔案
# --no-dev: 排除開發/測試套件 (如 pytest、ruff)，只裝 production 套件
# --no-install-project: 先不把當前專案當作套件安裝，可以最大化利用 Docker Layer Cache
RUN uv sync --frozen --no-dev --no-install-project

# ==========================================
# 第二階段：建立純淨的執行環境 (Runner)
# ==========================================
FROM python:3.12-slim

WORKDIR /app

# 拋棄混亂的 site-packages 複製！直接將整個 `.venv` 虛擬環境資料夾複製過來
COPY --from=builder /app/.venv /app/.venv

# 將虛擬環境的執行檔路徑放到系統最前端
# 這樣一來，後續執行 `python` 時，系統就會自動使用該虛擬環境，不需加 `uv run`
ENV PATH="/app/.venv/bin:$PATH"

# 複製專案所有程式碼
COPY . .

# 暴露埠號
EXPOSE 5500

# 執行資料庫遷移並啟動 Flask 應用程式
CMD [ "sh", "-c", "python migrate.py && python main.py" ]