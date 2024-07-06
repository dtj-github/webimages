from fastapi import FastAPI, Request # FastAPIとリクエストモジュールのインポート
from fastapi.responses import StreamingResponse # StreamingResponseのインポート
import matplotlib.pyplot as plt # Matplotlibのインポート
import io # バイナリストリームを扱うためのモジュールのインポート

app = FastAPI() # FastAPIアプリケーションの作成

@app.get("/plot") # GETリクエストを受け取るルートの定義
async def plot(request: Request):
    x = request.query_params.get('x', '1,2,3,4,5') # GETパラメータ'x'の取得、デフォルト値は'1,2,3,4,5'
    y = request.query_params.get('y', '1,4,9,16,25') # GETパラメータ'y'の取得、デフォルト値は'1,4,9,16,25'
    x = [int(i) for i in x.split(',')] # 'x'パラメータを整数リストに変換
    y = [int(i) for i in y.split(',')] # 'y'パラメータを整数リストに変換

    plt.figure() # 新しい図の作成
    plt.plot(x, y) # xとyのプロット
    plt.title("Sample Plot") # グラフのタイトル設定

    img = io.BytesIO() # バイナリストリームの作成
    plt.savefig(img, format='png') # バイナリストリームに画像を保存
    img.seek(0) # ストリームのポインタを先頭に移動

    return StreamingResponse(img, media_type='image/png') # クライエントに画像を返す
