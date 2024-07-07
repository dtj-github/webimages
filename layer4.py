import numpy as np
from scipy.optimize import curve_fit

def fit_set_dff(df):
    dff = df.copy() # 作業用dff
    dff["days"] = range(len(df)) # 開始日からの日数(=行番号)を格納
    dff["var"] = None # 偏差
    return dff

def fit_set_var(dff):
    ticker = dff.columns[0] # ticker名取得
    series_var = dff[ticker]/dff["center"] # 仮センターからの偏差を取る
    return series_var

def fit_set_bottom(dff, sep_num=10):
    # 準備
    dff_tmp = dff.copy() # コピー
    ticker = dff_tmp.columns[0] # ティッカー名取得
    block = int(len(dff_tmp)/sep_num) # 1ブロックあたりの行数(=日数)
    # 各区間における価格最低行(日)に目印をつける
    for i in range(0, len(dff_tmp), block): # indexで処理
        dff_section = dff_tmp.iloc[i:i+block-1, :] # 分割したdff
        min_section = dff_section[ticker].min() # 区間最小値(価格)
        index_name = dff_section[dff_section[ticker]==min_section].index[0] # 区間最小値のindex名を取得
        dff_tmp.at[index_name, "low_points"] = 1 # 該当行のlow_point列にフラグ1を立てる
    # 価格最低行(日)の中でも仮センターからの偏差が小さい方向に突出している2点を結ぶ
    dffl = dff_tmp[dff_tmp["low_points"]==1] # 区間最小価格の行を抽出
    dffl = dffl.sort_values("var") # 偏差が小さい順にソート
    x1, x2 = dffl.iat[0, dffl.columns.get_loc("days")], dffl.iat[1, dffl.columns.get_loc("days")] # 何日目か取得(xに相当)
    y1, y2 = dffl.iat[0, 0], dffl.iat[1, 0] # 価格を取得(yに相当)
    a,b = get_a_b(x1, y1, x2, y2) # y=(a**x)*bのa,b(傾きと切片)を取得
    series_bottom = (a**dff_tmp["days"])*b # bottom列に格納
    return series_bottom

def get_a_b(x1, y1, x2, y2):
    a = np.exp(np.log(y2/y1)/(x2-x1)) # y=(a^x)bをaについて解いたものを、exp(eに乗する）している
    b = y1/(a**x1) # y=(a^x)bをbについて解いたもの。
    return a,b

def fit_set_top(dff, max_i=100000):
    ticker = dff.columns[0] # ticker名を取得
    for i in range(max_i): # ちょっとずつbottomを上げていき、最上点を超えたらbreak
        rate = 1+i/10 # 1.0, 1.1, 1.2,...
        dff["top"] = dff["bottom"] * rate # bottomのrate倍をtopにいれる
        if (dff[ticker] < dff["top"]).all(): # もしすべての行でtopが上回ったら
            break # その時点で終了
    series_top = dff["top"] # topを返す
    return series_top

def fit_set_center(dff):
    series_center = (dff["top"]*dff["bottom"])**0.5 # 相乗平均を取る
    return series_center

def fit_adjust_dff(dff):
    dff = dff.drop(columns=["days", "var"]) # 不要列を削除
    dff = dff.iloc[:, [0,3,1,2]] # 並び替え
    return dff

def fit_exp(x_seq, y_seq):
    def func_to_log(x, a, b):
        return x*np.log(a) + np.log(b) # 元はy=(a^x)*bという式。log変形してln(y)=x*ln(a)+ln(b)
    def log_to_exp(x,a,b):
        return np.exp(x*np.log(a) + np.log(b)) # expで元の形（元の値）に戻している
    x_seq = x_seq.copy() # copy
    y_seq = y_seq.copy() # copy
    x_seq.replace(0, 0.000000001, inplace=True) # 0はエラーになるので、微小値に置換
    y_seq.replace(0, 0.000000001, inplace=True) # 0はエラーになるので、微小値に置換
    log_popt, log_pcov = curve_fit(func_to_log, x_seq, np.log(y_seq)) # yのlogをとった後のフィッティング。※log_popt=(a,b)
    series_fit_exp = log_to_exp(x_seq, *log_popt) # 元の値に戻す
    return series_fit_exp