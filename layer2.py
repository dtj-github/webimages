import base64 # base64

import layer3 as l3

def get_params(request):
    num_plots = int(request.query_params.get('num', '3'))
    return num_plots

def create_images(params):

    images = [] # 画像データを格納するリスト

    tickers = ["SOXL", "TECL", "SPXL", "COST", "LLY", "NVO", "ODFL", "PGR"] # 対象ティッカー
    df = l3.get_data(tickers) # ダウンロードする

    # 各tickerごとに処理
    for ticker in df.columns:
        dft = df.loc[:, [ticker]] # 対象列をdfとして抜き出す
        dft = l3.format_data(dft) # データの無い行を削除する、days行を追加
        dftf = l3.fit_band(dft) # バンドをフィットさせる
        image = l3.plot_log_chart(dftf) # plotして画像データを取得
        images.append(image) # imagesリストに追加

    return images


def make_html_content(images):
    html_content = "<html><body>" # HTMLの開始タグ
    for i, img in enumerate(images): # 各画像に対して
        img_base64 = base64.b64encode(img).decode("utf-8") # 画像をBase64エンコード
        html_content += f'<h2>Plot {i + 1}</h2><img src="data:image/png;base64,{img_base64}"/><br/>' # 画像をHTMLに埋め込む
    html_content += "</body></html>" # HTMLの終了タグ
    return html_content

