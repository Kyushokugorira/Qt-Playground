import os
import pickle
import sys
import random as r
import datetime as dt
import PySide6.QtWidgets as Qw
import PySide6.QtCore as Qc
import PySide6.QtTest as Qt

# カードガチャ関連 ####
card_t = ('SSR','SR','R','N') # タイプ
card_p = (1,10,20,25)         # 排出比
card_i = list(range(len(card_t))) # インデックス
def gacha():
  x = r.choices(card_i, k=1, weights=card_p)
  return x[0]

def gacha10():
  x = r.choices(card_i, k=10, weights=card_p)
  return x

# 時刻関連 ####
def get_datatime():
  t = dt.datetime.now() # 現在時刻の取得
  return t.strftime('%Y/%m/%d %H:%M:%S')

# MainWindowクラス定義 ####
class MainWindow(Qw.QMainWindow):
  
  def __init__(self):
    super().__init__() 
    self.setWindowTitle('MainWindow') 
    self.setGeometry(100, 50, 640, 240) 

    # ランクごとのカード所持数と総課金額の初期化
    self.card_counts = [0] * len(card_p)
    self.charges = 0

    #「実行」ボタンの生成と設定
    self.btn_run = Qw.QPushButton('実行',self)
    self.btn_run.setGeometry(10,10,100,20)
    self.btn_run.clicked.connect(self.btn_run_clicked)

    # 「10連」ボタンの生成と設定
    self.btn_run10 = Qw.QPushButton('10連実行',self)
    self.btn_run10.setGeometry(120,10,100,20)
    self.btn_run10.clicked.connect(self.btn_run10_clicked)

    #「クリア」ボタンの生成と設定
    self.btn_clear = Qw.QPushButton('クリア',self)
    self.btn_clear.setGeometry(230,10,100,20)
    self.btn_clear.clicked.connect(self.btn_clear_clicked)

    # テキストボックス
    self.tb_log = Qw.QTextEdit('',self)
    self.tb_log.setGeometry(10,40,620,170)
    self.tb_log.setReadOnly(True)
    self.tb_log.setPlaceholderText('(ここに実行ログを表示します)')

    # ステータスバー
    self.sb_status = Qw.QStatusBar()
    self.setStatusBar(self.sb_status)
    self.sb_status.setSizeGripEnabled(False)

    # データファイルが存在すれば読み込む
    self.data_file = './qt-05.dat'
    if os.path.isfile(self.data_file):
      with open(self.data_file,'rb') as file:
        data = pickle.load(file)
        self.card_counts = data['card_counts']
        self.charges = data['charges']
        self.update_status()
    else :
      self.sb_status.showMessage('プログラムを起動しました。')

  # 終了処理
  def closeEvent(self, event):
    with open(self.data_file,'wb') as file:
      data = {}
      data['card_counts'] = self.card_counts
      data['charges'] = self.charges
      pickle.dump(data, file)
      print('データファイルを更新セーブしました。')
    event.accept()

  #「実行」ボタンの押下処理
  def btn_run_clicked(self):
    idx = gacha()
    self.card_counts[idx]+=1  # カード所持数の更新
    self.charges += 300       # 課金総額の更新

    # プログレスバーダイアログの表示
    gacha_msg = ['  ++++++  ガチャ抽選中  ++++++  ',
                 '  ------  ガチャ抽選中  ------  ' ]
    p_bar = Qw.QProgressDialog(gacha_msg[0],None,0,100,self)
    p_bar.setWindowModality(Qc.Qt.WindowModality.WindowModal)
    p_bar.setWindowTitle('ガチャ抽選')
    p_bar.show()
    for p in range(101):
      p_bar.setValue(p)
      if p % 10 == 0:
        p_bar.setLabelText(gacha_msg[p//10%2])
      Qt.QTest.qWait(5)
    p_bar.close()

    # テキストボックスの表示を更新
    log = f'({get_datatime()})\n'
    log += f'【{card_t[idx]}】ランクのカードを1枚取得しました !! \n\n'
    log += self.tb_log.toPlainText()
    self.tb_log.setPlainText(log)

    # ステータスバーの表示を更新
    self.update_status()

  #「クリア」ボタンの押下処理
  def btn_clear_clicked(self):
    self.tb_log.setPlainText('')

  # ステータスバーの表示を更新
  def update_status(self):
    msg = ''
    for i in range(len(card_t)):
      msg += f'{card_t[i]} : {self.card_counts[i]}枚   '
    msg += f'課金総額 {self.charges:,} 円'
    self.sb_status.showMessage(msg)

  #「10連実行」ボタンの押下処理
  def btn_run10_clicked(self):
    idx = gacha10()
    for i in range(10):
      self.card_counts[idx[i]]+=1  # カード所持数の更新
      self.charges += 300       # 課金総額の更新

    # プログレスバーダイアログの表示
    gacha_msg = ['  ++++++  ガチャ抽選中  ++++++  ',
                 '  ------  ガチャ抽選中  ------  ' ]
    p_bar = Qw.QProgressDialog(gacha_msg[0],None,0,100,self)
    p_bar.setWindowModality(Qc.Qt.WindowModality.WindowModal)
    p_bar.setWindowTitle('ガチャ抽選')
    p_bar.show()
    for p in range(101):
      p_bar.setValue(p)
      if p % 10 == 0:
        p_bar.setLabelText(gacha_msg[p//10%2])
      Qt.QTest.qWait(5)
    p_bar.close()

    # テキストボックスの表示を更新
    for i in range (10):
        log = f'({get_datatime()})\n'
        log += f'【{card_t[idx[i]]}】ランクのカードを1枚取得しました !! \n\n'
        log += self.tb_log.toPlainText()
        self.tb_log.setPlainText(log)

    # ステータスバーの表示を更新
    self.update_status()

  #「クリア」ボタンの押下処理
  def btn_clear_clicked(self):
    self.tb_log.setPlainText('')

  # ステータスバーの表示を更新
  def update_status(self):
    msg = ''
    for i in range(len(card_t)):
      msg += f'{card_t[i]} : {self.card_counts[i]}枚   '
    msg += f'課金総額 {self.charges:,} 円'
    self.sb_status.showMessage(msg)
