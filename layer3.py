import matplotlib.pyplot as plt # Matplotlibのインポート
import io # バイナリストリームを扱うためのモジュールのインポート
import yfinance as yf
import pandas as pd

import layer4 as l4

# get data
def get_data(tickers):
    df = yf.download(tickers)["Adj Close"]  # 指定された期間のデータを取得
    df = df.loc[:, tickers] # 指定した順番に並べ替える
    return df

# format data
def format_data(df):
    df = df.dropna()          # NaNが存在する行をすべて削除
    df = df[(df != 0).all(1)] # 0が存在する行をすべて削除
    df["days"] = df.index     # index列をdays列に追加
    return df

# fit band
def fit_band(df):
    """
    n行1列のdfをインプットとし、n行4列のdffをアウトプットとする。
    価格列を元に、top/center/bottomのラインを計算して列追加する。
    ［ロジック］
    価格から仮センターをセットする。
        価格データに対し対数曲線で近似する。y=(a^x)b y=価格, a=傾き(1.01とか), x=開始日を0とする日数, b=切片。
        価格データの対数をとり、直線近似をしてから、np.expして元に戻す。
    偏差をセットする。
        直線近似の場合はy座標の引き算で行うが、対数近似ではy座標の割り算で行う。
        （点のy座標が仮センターのy座標の何倍か）
    bottom（サポートライン）をセットする。
        データを等分割（デフォルトで10）する。
        各ブロック内での最小値（最小価格）がある行（日）を見つける。
        その中でも、仮センターからの偏差が最も大きい2点を見つける。
        その2点については下に突出しているはずなので、対数線で結ぶ(y=(a^x)bのa,bを求める)
        a,bがわかったら、xを開始日からの日数として、yを計算し、bottomとする。
    topをセットする。
        bottomのラインをちょっとずつ上に上げていく（1.0倍、1.1倍、1.2倍...）
        値のすべてが、元の価格のすべてを上回ったとき、終了。
    centerをセットする。
        topとbottomの相乗平均を取る。(top*bottom)**0.5
        このとき、仮センターを上書きする。
    """

    dff = l4.fit_set_dff(df) # dfからdffを設定

    dff["center"] = l4.fit_exp(x_seq=dff["days"], y_seq=dff.iloc[:, 0]) # 仮センターをセット
    dff["var"]    = l4.fit_set_var(dff) # 偏差をセット

    dff["bottom"] = l4.fit_set_bottom(dff) # 順番厳守。まずbottom
    dff["top"]    = l4.fit_set_top(dff) # 次にtop
    dff["center"] = l4.fit_set_center(dff) # 最後にcenter

    dff = l4.fit_adjust_dff(dff) # 最後の調整

    return dff

# plot log chart
def plot_log_chart(df):

    df.index = pd.to_datetime(df.index) # indexのyyyy-mm-ddを文字列からdatetimeに変換（plot時に自動調整できるように）
    ticker = df.columns[0] # ticker名

    # プロット
    fig, ax = plt.subplots() # 初期設定

    for column in df.columns: # 各列
        ax.plot(df.index, df[column], label=column) # x=index, y=各列
    ax.grid() # グリッド線
    ax.set_title(f"{ticker} y-axis log scale") # title
    ax.legend(loc="upper left") # 凡例の位置
    ax.set_yscale("log") # y軸log

    img = io.BytesIO() # バイナリストリームの作成
    plt.savefig(img, format='png') # バイナリストリームに画像を保存
    img.seek(0) # ストリームのポインタを先頭に移動
    image = img.getvalue() # imageデータを取得
    return image








