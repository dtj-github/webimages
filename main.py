from fastapi import FastAPI, Request # FastAPIとリクエストモジュールのインポート
from fastapi.responses import HTMLResponse # StreamingResponseとHTMLResponseのインポート

import layer1 as l1

app = FastAPI() # FastAPIアプリケーションの作成

@app.get("/plots", response_class=HTMLResponse) # GETリクエストを受け取り、HTMLレスポンスを返すルートの定義
async def plots(request: Request):
    html_content = l1.create_html_content(request)
    return HTMLResponse(content=html_content) # クライエントにHTMLレスポンスを返す

# uvicorn main:app --reload
# http://127.0.0.1:8000/plots