import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageGrab, ImageDraw, ImageTk



# お絵描きエリアの管理用クラス
#   tk.Canvas を継承しているわけではなく，単に外から操作するだけ
class PaintMng():
    def __init__(self, canv):
        self.canv = canv
        self.sx, self.sy = canv.winfo_width(), canv.winfo_height()
        self.clickToggle = False
        self.paintEnable = True
        self.oldX, self.oldY = None, None

        # キャンバス関係の設定
        self.im = Image.new("RGB", (self.sx, self.sy), "white")
        self.draw = ImageDraw.Draw(self.im)

        # 指定したキャンバス，ウィンドウに対するキーチェック
        canv.bind("<1>", self.clickSwitch)      # 左クリックされた時
        canv.bind("<Motion>", self.mouseMove)   # マウスが移動した時
    
    # 線を描くか描かないかを切り換える関数
    def clickSwitch(self, event):
        if (self.clickToggle):
            self.clickToggle = False
        else:
            self.clickToggle = True
    
    # 描画とマウス座標の管理を行う関数
    def mouseMove(self, event):
        if (self.paintEnable):
            if (self.clickToggle):
                if (self.oldX and self.oldY):
                    self.canv.create_line(self.oldX, self.oldY, event.x, event.y, width=5.0, fill="black", capstyle=tk.ROUND, smooth=tk.TRUE, splinesteps=36, tag="paint")
                self.oldX, self.oldY = event.x, event.y
            else:
                self.oldX, self.oldY = None, None
    
    # キャンバス内の線を消去する関数
    def clearCanvas(self, reset=False):
        if (self.paintEnable or reset):
            # 消した直後から線が描かれないよう，強制的に描かない設定にする
            self.clickToggle = False
            self.oldX, self.oldY = None, None
            #　タグ指定で線のみを消去
            self.canv.delete("paint")
    
    def setPaintEnable(self, bool):
        self.paintEnable = bool



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
        """
        
        # スペースキーでキャンバスを消去
        def clearAll(reset=False):
            tutorialPaintMng.clearCanvas(reset)
            drawingPaintMng.clearCanvas(reset)
        self.bind("<KeyPress-space>", clearAll)

# title --------------------------------------------------------------------------------------------------------------------------------
        # 遷移用関数の設定
        def toTutorialProc(dummy):
            clearAll(reset=True)
            self.changePage(self.tutorialFrame)
        # フレームの設定
        self.titleFrame = tk.Frame(bg="white")
        self.titleFrame.grid(row=0, column=0, sticky="nsew")
        # 画像の読み込み
        self.titleBackImage = ImageTk.PhotoImage(file="./img/title.png")
        # キャンバスの設定
        self.titleCanvas = tk.Canvas(self.titleFrame, bg="white")
        self.titleCanvas.create_image(hW, hH, image=self.titleBackImage)
        self.titleCanvas.create_text(hW, hH + 400, text="まばたきで開始", font=("helvetica", "36"))
        self.titleCanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # キャンバス( 画面のどこか )をクリックしたらチュートリアルに遷移
        self.titleCanvas.bind("<1>", toTutorialProc)
        # ボタンの設定
        self.exitBtn = tk.Button(self.titleFrame, text="終了", command=self.exitProc)
        self.exitBtn.place(x=fW-60, y=fH-35, width=50, height=25)
        """
        # 使わなかったボタン
        self.toTutorialBtn = tk.Button(self.titleFrame, text="スタート", command=lambda: self.changePage(self.tutorialFrame))
        self.toTutorialBtn.pack(anchor=tk.N, ipadx=150, ipady=100, pady=100)
        """

# tutorial --------------------------------------------------------------------------------------------------------------------------------
        # 遷移用関数の設定
        def toThemeProc():
            self.changePage(self.themeFrame)
            # お題と選択肢を設定
            self.themeCountdownLabel.config(text="")
            self.themeImage = ImageTk.PhotoImage(file="./theme/neko.png")
            #self.after(1500, announceTheme)
            self.after(1, announceTheme)  # デバッグ用
        # フレームの設定
        self.tutorialFrame = tk.Frame(bg="light gray")
        self.tutorialFrame.grid(row=0, column=0, sticky="nsew")
        # キャンバスの設定
        self.tutorialCanvas = tk.Canvas(self.tutorialFrame, width=fW, height=fH-120, bg="white")
        self.tutorialCanvas.create_text(hW, 40, text="練習", font=("helvetica", "48"), fill="gray")
        self.tutorialCanvas.create_text(hW, 100, text="まばたきで  描く・描かない  の切り換え", font=("helvetica", "30"), fill="gray")
        self.tutorialCanvas.create_text(hW, 150, text="スペースキーで全消し", font=("helvetica", "30"), fill="gray")
        self.tutorialCanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # お絵描きキャンバスとして管理
        tutorialPaintMng = PaintMng(canv=self.tutorialCanvas)
        # ボタンの設定
        #self.toThemeBtn = tk.Button(self.tutorialFrame, text="練習を終わる", command=lambda: self.changePage(self.themeFrame))
        self.toThemeBtn = tk.Button(self.tutorialFrame, text="練習を終わる", command=toThemeProc)
        self.toThemeBtn.pack(side=tk.BOTTOM, ipadx=300, ipady=40)

# theme --------------------------------------------------------------------------------------------------------------------------------
        # 遷移・表示用関数の設定
        themeResize = (524, 450)
        def announceTheme():
            self.themeImage = ImageTk.PhotoImage(Image.open("./theme/neko.png").resize(themeResize))
            self.themeCanvas.create_image(1150, 580, image=self.themeImage)
            self.themeCanvas.create_text(640, 530, text="チューリップ", font=("Helvetica", "50"))
            # 9 秒のカウントダウン
            #self.after(1500, showThemeCountdown, 9)
            self.after(1500, showThemeCountdown, 2)  # デバッグ用
        
        def showThemeCountdown(time):
            if (time < 1):
                # キャンバスに絵を描けるようにする
                drawingPaintMng.setPaintEnable(True)
                # 60 秒のタイムリミット設定
                #drawingTimer(60)
                drawingTimer(3)  # デバッグ用
                self.changePage(self.drawingFrame)
            else:
                self.themeCountdownLabel.config(text="スタートまで...  {}".format(time))
                self.after(1000, showThemeCountdown, time-1)
        
        # フレームの設定
        self.themeFrame = tk.Frame(bg="white")
        self.themeFrame.grid(row=0, column=0, sticky="nsew")
        # 画像の読み込み
        self.themeBackImage = ImageTk.PhotoImage(file="./img/theme.png")
        self.themeImage = ImageTk.PhotoImage(Image.new("RGB", themeResize, "#D6D0CE"))  # とりあえず空イメージを設定しておく
        iThemeW, iThemeH = self.themeImage.width(), self.themeImage.height()
        # キャンバスの設定
        self.themeCanvas = tk.Canvas(self.themeFrame, bg="light gray")
        self.themeCanvas.create_image(hW, hH, image=self.themeBackImage)
        self.themeCanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # ラベルの設定
        self.themeCountdownLabel = tk.Label(self.themeFrame, font=("Helvetica", "36"), bg="#D6D0CE")
        self.themeCountdownLabel.place(x=965, y=220, width=420, height=65)
        """
        # 使わなかったボタン
        self.toDrawingBtn = tk.Button(self.themeSubFrame, text="next", command=lambda: self.changePage(self.drawingFrame))
        self.toDrawingBtn.pack()
        """

# drawing --------------------------------------------------------------------------------------------------------------------------------
        # 遷移・表示用関数の設定
        def drawingTimer(time):
            if (time < 1):
                # キャンバスに絵を描けなくする
                drawingPaintMng.setPaintEnable(False)
                # 終了～！みたいな演出
                self.drawingTimerLabel.config(text="終了！")
                # 描いた絵をキャプチャして貼り付け
                self.drawingCapture = ImageTk.PhotoImage(self.canvasCapture(self.drawingCanvas).resize((945, 528)))
                self.answerCanvas.create_image(991, 329, image=self.drawingCapture)
                # 3 秒後にページ遷移
                #self.after(3000, self.changePage, self.answerFrame)
                self.after(1, self.changePage, self.answerFrame)  # デバッグ用
            else:
                self.drawingTimerLabel.config(text="残り{}秒".format(time))
                self.after(1000, drawingTimer, time-1)
        
        # フレームの設定
        self.drawingFrame = tk.Frame(bg="white")
        self.drawingFrame.grid(row=0, column=0, sticky="nsew")
        # ラベルの設定
        self.drawingTimerLabel = tk.Label(self.drawingFrame, font=("Helvetica", "35"), fg="gray", bg="light gray")
        self.drawingTimerLabel.pack(side=tk.BOTTOM, fill=tk.X, ipady=10)
        # キャンバスの設定
        self.drawingCanvas = tk.Canvas(self.drawingFrame, width=fW, height=fH-120, bg="white")
        iDrawingW, iDrawingH = self.drawingCanvas.winfo_width(), self.drawingCanvas.winfo_height()
        self.drawingCanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # キャプチャ画像を格納するオブジェクトを生成しておく
        self.drawingCapture = ImageTk.PhotoImage(Image.new("RGB", (iDrawingW, iDrawingH), "white"))
        # お絵描きキャンバスとして管理
        drawingPaintMng = PaintMng(canv=self.drawingCanvas)
        """
        # 使わなかったボタン
        self.toAnswerBtn = tk.Button(self.drawingFrame, text="next", command=lambda: self.changePage(self.answerFrame))
        self.toAnswerBtn.pack()
        """

# answer　--------------------------------------------------------------------------------------------------------------------------------
        # フレームの設定
        self.answerFrame = tk.Frame(bg="white")
        self.answerFrame.grid(row=0, column=0, sticky="nsew")
        # 画像の読み込み
        self.answerBackImage = ImageTk.PhotoImage(file="./img/answer.png")
        # キャンバスの設定
        self.answerCanvas = tk.Canvas(self.answerFrame, bg="white")
        self.answerCanvas.create_image(hW, hH, image=self.answerBackImage)
        #self.answerCanvas.create_text(hW, 80, text="回答選択", font=("helvetica", "48"))
        self.answerCanvas.place(x=0, y=0, width=fW, height=fH)
        # リストに選択肢の情報をセット
        ansResize = (356, 300)
        ansLabelSize = (356, 91)
        self.answerChoices = [  # とりあえず全部ネコ
            [Image.open("./theme/neko.png"), (278, 662), "イヌ"],
            [Image.open("./theme/neko.png"), (812, 662), "ネコ"],
            [Image.open("./theme/neko.png"), (1323, 662), "チューリップ"]
        ]
        correctIndex = 1
        self.checkThemeImage = ImageTk.PhotoImage(self.answerChoices[correctIndex][0].resize(themeResize))
        # ボタンが押された時の動作を定義する
        def answerCallback(id):
            def x():
                # 選択によって背景画像を変える
                if (id == correctIndex):    # 正解
                    self.checkBackImage = ImageTk.PhotoImage(file="./img/correct.png")
                else:                       # 不正解
                    self.checkBackImage = ImageTk.PhotoImage(file="./img/incorrect.png")
                # checkCanvas に画像や文字を配置
                self.checkCanvas.create_image(hW, hH, image=self.checkBackImage)
                self.checkCanvas.create_text(533, 810, text=self.answerChoices[correctIndex][2], font=("helvetica", "50"), fill="black")
                self.checkCanvas.create_image(1200, 770, image=self.checkThemeImage)
                self.changePage(self.checkFrame)
            return x
        # ボタンの設定
        cntr = 0
        self.answerChoiceBtn = list()
        self.answerChoiceLabel = list()
        self.answerChoiceImage = list()
        for im, pos, name in self.answerChoices:
            self.answerChoiceImage.append(ImageTk.PhotoImage(im.resize(ansResize)))
            self.answerChoiceBtn.append(tk.Button(self.answerFrame, command=answerCallback(cntr), image=self.answerChoiceImage[cntr]))
            self.answerChoiceLabel.append(tk.Label(self.answerFrame, text=name, font=("Helvetica", "36"), fg="black", bg="light gray"))
            self.answerChoiceBtn[cntr].place(x=pos[0], y=pos[1], width=ansResize[0], height=ansResize[1])
            self.answerChoiceLabel[cntr].place(x=pos[0], y=pos[1]+ansResize[1], width=ansLabelSize[0], height=ansLabelSize[1])
            cntr += 1
        """
        # 使わなかったボタン
        self.toCheckBtn = tk.Button(self.answerFrame, text="正解へ", command=lambda: self.changePage(self.checkFrame))
        self.toCheckBtn.place(x=fW-200, y=fH-100, width=100, height=50)
        #self.toCheckBtn.pack(side=tk.BOTTOM, anchor=tk.E, ipadx=100, ipady=30, padx=20, pady=20)
        """

# check --------------------------------------------------------------------------------------------------------------------------------
        # フレームの設定
        self.checkFrame = tk.Frame(bg="white")
        self.checkFrame.grid(row=0, column=0, sticky="nsew")
        # キャンバスの設定
        self.checkCanvas = tk.Canvas(self.checkFrame, bg="white")
        self.checkCanvas.place(x=0, y=0, width=fW, height=fH)
        self.checkBackImage = ImageTk.PhotoImage(Image.new("RGB", ansResize, "white"))  # とりあえず空イメージを設定しておく
        # ボタンの設定
        self.toTitleBtn = tk.Button(self.checkFrame, text="終わる", command=lambda: self.changePage(self.titleFrame))
        self.toTitleBtn.place(x=fW-220, y=fH-70, width=200, height=50)
        
        # タイトル画面を最前面にする
        self.titleFrame.tkraise()

    # 画面遷移する関数
    # page: 遷移先のフレーム
    def changePage(self, page):
        page.tkraise()

    # キャンバス内をキャプチャする関数
    # c: キャプチャするキャンバスオブジェクト
    def canvasCapture(self, c):
        """
        # 一応 2 種類のやり方を用意してある
        x= c.winfo_rootx() + c.winfo_x()
        y= c.winfo_rooty() + c.winfo_y()
        x1= x + c.winfo_width()
        y1= y + c.winfo_height()
        return ImageGrab.grab().crop((x, y, x1, y1))
        """
        wx, wy = c.winfo_rootx(), c.winfo_rooty()
        inner_w, inner_h = int(c.cget("width")), int(c.cget("height"))
        outer_w, outer_h = c.winfo_width(), c.winfo_height()
        ox, oy = (outer_w-inner_w)//2, (outer_h-inner_h)//2
        x0, x1, y0, y1 = 0, inner_w, 0, inner_h
        return ImageGrab.grab((wx+x0+ox, wy+y0+oy, wx+x1+ox, wy+y1+oy))

    # 終了時に呼び出される関数
    def exitProc(self):
        if (messagebox.askyesno("確認", "終了しますか？")):
            self.quit()



if __name__ == "__main__":
    app = App()
    app.mainloop()