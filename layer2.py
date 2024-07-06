import matplotlib.pyplot as plt # Matplotlibのインポート
import io # バイナリストリームを扱うためのモジュールのインポート
import base64 # base64

def get_params(request):
    num_plots = int(request.query_params.get('num', '3'))
    return num_plots

def create_images(num_plots):
    images = [] # 画像データを格納するリスト
    for i in range(num_plots): # 指定された数のプロットを作成
        x = [1, 2, 3, 4, 5] # x軸のデータ
        y = [(j + i) ** 2 for j in x] # y軸のデータ

        plt.figure() # 新しい図の作成
        plt.plot(x, y) # xとyのプロット
        plt.title(f"Sample Plot {i + 1}") # グラフのタイトル設定

        img = io.BytesIO() # バイナリストリームの作成
        plt.savefig(img, format='png') # バイナリストリームに画像を保存
        img.seek(0) # ストリームのポインタを先頭に移動
        images.append(img.getvalue()) # 画像データをリストに追加
    return images

def make_html_content(images):
    html_content = "<html><body>" # HTMLの開始タグ
    for i, img in enumerate(images): # 各画像に対して
        img_base64 = base64.b64encode(img).decode('utf-8') # 画像をBase64エンコード
        html_content += f'<h2>Plot {i + 1}</h2><img src="data:image/png;base64,{img_base64}"/><br/>' # 画像をHTMLに埋め込む
    html_content += "</body></html>" # HTMLの終了タグ
    return html_content