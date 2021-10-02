import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk

# お絵描きエリアの管理用クラス
#   tk.Canvas を継承しているわけではなく，単に外から操作するだけ
class PaintMng():
    def __init__(self, master, canv):
        self.master = master
        self.canv = canv
        self.sx, self.sy = canv.winfo_width(), canv.winfo_height()
        self.clickToggle = False
        self.oldX, self.oldY = None, None

        # キャンバス関係の設定
        self.im = Image.new("RGB", (self.sx, self.sy), "white")
        self.draw = ImageDraw.Draw(self.im)

        # 指定したキャンバス，ウィンドウに対するキーチェック
        canv.bind("<1>", self.clickSwitch)                  # 左クリックされた時
        canv.bind("<Motion>", self.mouseMove)               # マウスが移動した時
        master.bind("<KeyPress-space>", self.clearCanvas)   # スペースキーが押された時
    
    # 線を描くか描かないかを切り換える関数
    def clickSwitch(self, event):
        if (self.clickToggle):
            self.clickToggle = False
        else:
            self.clickToggle = True
    
    # 描画とマウス座標の管理を行う関数
    def mouseMove(self, event):
        if (self.clickToggle):
            if (self.oldX and self.oldY):
                self.canv.create_line(self.oldX, self.oldY, event.x, event.y, width=5.0, fill="black", capstyle=tk.ROUND, smooth=tk.TRUE, splinesteps=36, tag="paint")
            self.oldX, self.oldY = event.x, event.y
        else:
            self.oldX, self.oldY = None, None
    
    # キャンバス内の線を消去する関数
    def clearCanvas(self, event):
        # 消した直後から線が描かれないよう，強制的に描かない設定にする
        self.clickToggle = False
        self.oldX, self.oldY = None, None
        #　タグ指定で線のみを消去
        self.canv.delete("paint")



# 本体のクラス
class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # ウィンドウに関する設定
        self.title("oekaki")
        # ウィンドウのグリッドを 1 x 1 にする
        #   この処理をコメントアウトすると配置がずれる
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        """
        # フルスクリーン表示
        self.attributes("-fullscreen", True)
        fW = self.winfo_screenwidth()
        hW = fW / 2
        fH = self.winfo_screenheight()
        hH = fH / 2
        """
        # デバッグ用
        self.geometry("1920x1080")
        fW = 1920
        hW = fW / 2
        fH = 1080
        hH = fH / 2

        # title
        # フレームの設定
        self.titleFrame = tk.Frame(bg="white")
        self.titleFrame.grid(row=0, column=0, sticky="nsew")
        # 画像の読み込み
        self.titleImage = ImageTk.PhotoImage(file="./img/title.png")
        # キャンバスの設定
        self.titleCanvas = tk.Canvas(self.titleFrame, bg="white")
        self.titleCanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.titleCanvas.create_image(hW, hH, image=self.titleImage)
        self.titleCanvas.create_text(hW, hH + 400, text="まばたきで開始", font=("helvetica", "36"))
        # キャンバス( 画面のどこか )をクリックしたらチュートリアルに遷移
        self.titleCanvas.bind("<1>", lambda x: self.changePage(self.tutorialFrame))
        """
        # 使わなかったボタン
        self.toTutorialBtn = tk.Button(self.titleFrame, text="スタート", command=lambda: self.changePage(self.tutorialFrame))
        self.toTutorialBtn.pack(anchor=tk.N, ipadx=150, ipady=100, pady=100)
        self.exitBtn = tk.Button(self.titleFrame, text="終了", command=self.exitProc)
        self.exitBtn.pack(anchor=tk.E, padx=10, pady=10)
        """

        # tutorial
        # フレームの設定
        self.tutorialFrame = tk.Frame(bg="light gray")
        self.tutorialFrame.grid(row=0, column=0, sticky="nsew")
        # キャンバスの設定
        self.tutorialCanvas = tk.Canvas(self.tutorialFrame, width=fW, height=fH-120, bg="white")
        self.tutorialCanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.tutorialCanvas.create_text(hW, 40, text="練習", font=("helvetica", "48"), fill="gray")
        self.tutorialCanvas.create_text(hW, 100, text="まばたきで  描く・描かない  の切り換え", font=("helvetica", "30"), fill="gray")
        self.tutorialCanvas.create_text(hW, 150, text="スペースキーで全消し", font=("helvetica", "30"), fill="gray")
        # お絵描きキャンバスとして管理
        tutorialPaintMng = PaintMng(master=self, canv=self.tutorialCanvas)
        # ボタンの設定
        self.toThemeBtn = tk.Button(self.tutorialFrame, text="練習を終わる", command=lambda: self.changePage(self.themeFrame))
        self.toThemeBtn.pack(side=tk.BOTTOM, ipadx=300, ipady=40)

        # theme
        self.themeFrame = tk.Frame(bg="white")
        self.themeFrame.grid(row=0, column=0, sticky="nsew")
        self.themeOdaihaLabel = tk.Label(self.themeFrame, text="お題は", font=("Helvetica", "48"), relief="ridge", borderwidth=2, bg="white")
        self.themeOdaihaLabel.grid(row=0, column=0)
        self.themeTitleLabel = tk.Label(self.themeFrame, text="〇〇", font=("Helvetica", "48"), relief="ridge", borderwidth=2, bg="white")
        self.themeTitleLabel.grid(row=1, column=1)
        self.toDrawingBtn = tk.Button(self.themeFrame, text="next", command=lambda: self.changePage(self.drawingFrame))
        #self.toDrawingBtn.pack()

        # drawing
        self.drawingFrame = tk.Frame()
        self.drawingFrame.grid(row=0, column=0, sticky="nsew")
        self.drawingLabel = tk.Label(self.drawingFrame, text="お絵描き", font=("Helvetica", "35"))
        self.drawingLabel.pack(anchor='center', expand=True)
        self.toAnswerBtn = tk.Button(self.drawingFrame, text="next", command=lambda: self.changePage(self.answerFrame))
        self.toAnswerBtn.pack()

        # answer
        self.answerFrame = tk.Frame()
        self.answerFrame.grid(row=0, column=0, sticky="nsew")
        self.answerLabel = tk.Label(self.answerFrame, text="回答選択", font=("Helvetica", "35"))
        self.answerLabel.pack(anchor='center', expand=True)
        self.toCheckBtn = tk.Button(self.answerFrame, text="next", command=lambda: self.changePage(self.checkFrame))
        self.toCheckBtn.pack()

        # check
        self.checkFrame = tk.Frame()
        self.checkFrame.grid(row=0, column=0, sticky="nsew")
        self.checkLabel = tk.Label(self.checkFrame, text="正解は〇〇！", font=("Helvetica", "35"))
        self.checkLabel.pack(anchor='center', expand=True)
        self.toTitleCBtn = tk.Button(self.checkFrame, text="next", command=lambda: self.changePage(self.titleFrame))
        self.toTitleCBtn.pack()

        # タイトル画面を最前面にする
        self.themeFrame.tkraise()

    # 画面遷移する関数
    # page: 遷移先のフレーム
    def changePage(self, page):
        page.tkraise()
    
    # 終了時に呼び出される関数
    def exitProc(self):
        if (messagebox.askyesno("確認", "終了しますか？")):
            self.quit()



if __name__ == "__main__":
    app = App()
    app.mainloop()