"""Simplified Chinese -> Traditional Chinese (Taiwan, with Taiwan phrases).
Follows OpenCC's s2twp chain with plain maximum-forward-matching:
  STPhrases/STCharacters -> TWPhrases -> TWVariants -> Flipper-specific overrides.
Usage as module: convert(text). As script: s2twp.py <opencc_dict_dir> file... (in place)
"""
import os, re, sys

DICT_DIR = os.environ.get('OPENCC_DICT', os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                      '..', 'opencc', 'data', 'dictionary'))

def _load(name):
    d = {}
    with open(os.path.join(DICT_DIR, name), encoding='utf-8') as f:
        for line in f:
            if not line.strip() or line.startswith('#'): continue
            k, v = line.rstrip('\n').split('\t', 1)
            d[k] = v.split(' ')[0]
    return d

ST = _load('STPhrases.txt'); ST_CHARS = _load('STCharacters.txt')
TW = _load('TWPhrases.txt'); TWV = _load('TWVariants.txt')
for k, v in ST_CHARS.items(): ST.setdefault(k, v)
MAXST = max(map(len, ST)); MAXTW = max(map(len, TW))

# Taiwan wording for terms OpenCC leaves in mainland usage (applied last, longest first).
OVERRIDES = {
    '密鑰': '金鑰', '扇區': '磁區', '讀卡器': '讀卡機', '固件': '韌體', '激活': '啟用',
    '屏幕': '螢幕', '熒幕': '螢幕', '信號': '訊號', '視頻': '影片', '音頻': '音訊',
    '幀率': '影格率', '緩存': '快取', '默認': '預設', '設置': '設定', '菜單': '選單',
    '保存': '儲存', '文件夾': '資料夾', '文件': '檔案', '數據': '資料', '程序': '程式',
    '軟件': '軟體', '硬件': '硬體', '內存': '記憶體', '網絡': '網路', '搜索': '搜尋',
    '加載': '載入', '鏈接': '連結', '鏈路': '鏈路', '接口': '介面', '界面': '介面',
    '用戶': '使用者', '信息': '資訊', '消息': '訊息', '打印': '列印', '二進制': '二進位',
    '十六進制': '十六進位', '十進制': '十進位', '字節': '位元組', '比特': '位元',
    '模塊': '模組', '端口': '埠', '串口': '序列埠', '服務器': '伺服器', '客戶端': '用戶端',
    '電量': '電量', '充電中': '充電中', '刷新': '重新整理', '粘貼': '貼上', '剪切': '剪下',
    '複製': '複製', '重命名': '重新命名', '新建': '新增', '創建': '建立', '運行': '執行',
    '應用程序': '應用程式', '質量': '品質', '分辨率': '解析度', '像素': '像素',
    '支持': '支援', '默認值': '預設值', '自定義': '自訂', '頻道': '頻道', '藍牙': '藍牙',
    '遙控器': '遙控器', '攔截': '攔截', '捕獲': '擷取', '提取': '擷取', '導出': '匯出',
    '導入': '匯入', '卸載': '卸載', '掛載': '掛載', '格式化': '格式化', '光標': '游標',
    '鼠標': '滑鼠', '鍵盤佈局': '鍵盤配置', '佈局': '配置', '在線': '線上', '離線': '離線',
    '登錄': '登入', '註銷': '登出', '賬戶': '帳戶', '賬號': '帳號', '短信': '簡訊',
    '計算機': '電腦', '筆記本': '筆電', '激光': '雷射',
    '電平': '電位', '晶振': '晶體振盪器', '閃存': '快閃記憶體', '存儲': '儲存', '存儲卡': '記憶卡',
    '日誌': '日誌', '缺省': '預設', '源代碼': '原始碼', '代碼': '程式碼', '算法': '演算法',
    '協議': '協定', '寄存器': '暫存器', '線程': '執行緒', '進程': '處理程序', '調試': '除錯',
    '回調': '回呼', '參數': '參數', '字符串': '字串', '字符': '字元', '數組': '陣列',
    '指針': '指標', '對象': '物件', '變量': '變數', '函數': '函式', '項目': '專案',
    '丟失': '遺失',
    # undo OpenCC IT phrases that are odd or needlessly long on a 128px screen
    '擴充套件': '擴充', '解除安裝': '卸載', '全域性': '全域', '進位制': '進位', '指令碼': '腳本',
    '對話方塊': '對話框', '訪問': '存取', '佔用': '佔用', '擦除': '清除', '視圖': '檢視', '數字標牌': '數位看板',
}
OV_KEYS = sorted(OVERRIDES, key=len, reverse=True)
MAXOV = max(map(len, OV_KEYS))

def _mfm(text, table, maxlen):
    out = []; i = 0; n = len(text)
    while i < n:
        for L in range(min(maxlen, n - i), 0, -1):
            seg = text[i:i + L]
            if seg in table:
                out.append(table[seg]); i += L; break
        else:
            out.append(text[i]); i += 1
    return ''.join(out)

def convert(text):
    t = _mfm(text, ST, MAXST)
    t = _mfm(t, TW, MAXTW)
    t = ''.join(TWV.get(c, c) for c in t)
    t = _mfm(t, OVERRIDES, MAXOV)
    return t

CJK_RUN = re.compile(r'[⺀-鿿豈-﫿　-〿＀-￯]+')

def convert_mixed(s):
    """Convert only CJK runs; ASCII (code, format specifiers) is untouched."""
    return CJK_RUN.sub(lambda m: convert(m.group(0)), s)

if __name__ == '__main__':
    changed = 0
    for p in sys.argv[1:]:
        try:
            s = open(p, encoding='utf-8').read()
        except (UnicodeDecodeError, IsADirectoryError):
            continue
        n = convert_mixed(s)
        if n != s:
            open(p, 'w', encoding='utf-8').write(n); changed += 1
    print('converted files:', changed)
