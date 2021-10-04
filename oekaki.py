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
    def clearCanvas(self):
        if (self.paintEnable):
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
        def clearAll(x):
            print("clear")
            tutorialPaintMng.clearCanvas()
            drawingPaintMng.clearCanvas()
        self.bind("<KeyPress-space>", clearAll)

# title --------------------------------------------------------------------------------------------------------------------------------
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
        self.titleCanvas.bind("<1>", lambda x: self.changePage(self.tutorialFrame))
        """
        # 使わなかったボタン
        self.toTutorialBtn = tk.Button(self.titleFrame, text="スタート", command=lambda: self.changePage(self.tutorialFrame))
        self.toTutorialBtn.pack(anchor=tk.N, ipadx=150, ipady=100, pady=100)
        self.exitBtn = tk.Button(self.titleFrame, text="終了", command=self.exitProc)
        self.exitBtn.pack(anchor=tk.E, padx=10, pady=10)
        """

# tutorial --------------------------------------------------------------------------------------------------------------------------------
        # 遷移用関数の設定
        self.answerChoices = list()
        def toThemeProc():
            self.changePage(self.themeFrame)
            # お題と選択肢を設定
            self.after(1500, announceTheme)
            #self.after(10, announceTheme)  # デバッグ用
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
        # 表示用関数の設定
        def announceTheme():
            self.themeCanvas.create_image(iThemeW/2, iThemeH/2, image=self.themeImage)
            self.themeTitleLabel.config(text="ネコ")
            # 9 秒のカウントダウン
            self.after(1500, showThemeCountdown, 9)
        def showThemeCountdown(time):
            if (time < 1):
                # 60 秒のタイムリミット設定
                drawingTimer(60)
                self.changePage(self.drawingFrame)
            else:
                self.themeCountdownLabel.config(text="スタートまで...  {}".format(time))
                self.after(1000, showThemeCountdown, time-1)
        # フレームの設定
        self.themeFrame = tk.Frame(bg="white")
        self.themeFrame.grid(row=0, column=0, sticky="nsew")
        self.themeSubFrame = tk.Frame(master=self.themeFrame, bg="white")
        self.themeSubFrame.pack(anchor=tk.CENTER, pady=200)
        # 画像の読み込み
        self.themeImage = ImageTk.PhotoImage(file="./theme/neko.png")
        iThemeW, iThemeH = self.themeImage.width(), self.themeImage.height()
        # ラベルの設定
        self.themeOdaihaLabel = tk.Label(self.themeSubFrame, text="お題は", font=("Helvetica", "48"), relief="ridge", borderwidth=0, bg="white")
        self.themeOdaihaLabel.grid(row=0, column=0, pady=20, sticky=tk.W+tk.E)
        self.themeTitleLabel = tk.Label(self.themeSubFrame, width=10, font=("Helvetica", "72"), relief="ridge", borderwidth=0, bg="white")
        self.themeTitleLabel.grid(row=1, column=1, padx=100, sticky=tk.N+tk.S)
        self.themeCountdownLabel = tk.Label(self.themeSubFrame, width=10, font=("Helvetica", "48"), relief="ridge", borderwidth=0, fg="gray", bg="white")
        self.themeCountdownLabel.grid(row=0, column=1, sticky=tk.W+tk.E)
        # キャンバスの設定
        self.themeCanvas = tk.Canvas(self.themeSubFrame, bg="light gray", width=iThemeW, height=iThemeH)
        self.themeCanvas.grid(row=1, column=0)
        """
        # 使わなかったボタン
        self.toDrawingBtn = tk.Button(self.themeSubFrame, text="next", command=lambda: self.changePage(self.drawingFrame))
        self.toDrawingBtn.pack()
        """

# drawing --------------------------------------------------------------------------------------------------------------------------------
        # 表示用関数の設定
        def drawingTimer(time):
            if (time < 1):
                # 終了～！みたいな演出
                drawingPaintMng.setPaintEnable(False)
                self.drawingTimerLabel.config(text="終了！")
                # 描いた絵をキャプチャして貼り付け
                self.drawingCapture = ImageTk.PhotoImage(self.canvasCapture(self.drawingCanvas).resize((945, 528)))
                self.answerCanvas.create_image(991, 329, image=self.drawingCapture)
                # 3 秒後にページ遷移
                #self.after(3000, self.changePage, self.answerFrame)
                self.after(10, self.changePage, self.answerFrame)  # デバッグ用
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
        self.answerCanvas = tk.Canvas(self.answerFrame, bg="white", width=iDrawingW, height=iDrawingH)
        self.answerCanvas.create_image(hW, hH, image=self.answerBackImage)
        #self.answerCanvas.create_text(hW, 80, text="回答選択", font=("helvetica", "48"))
        self.answerCanvas.place(x=0, y=0, width=fW, height=fH)
        # リストに選択肢の情報をセット
        ansResize = (356, 300)
        ansLabelSize = (356, 91)
        self.answerChoices = [  # とりあえず全部ネコ
            [ImageTk.PhotoImage(Image.open("./theme/neko.png").resize(ansResize)), (278, 662), "イヌ"],
            [ImageTk.PhotoImage(Image.open("./theme/neko.png").resize(ansResize)), (812, 662), "ネコ"],
            [ImageTk.PhotoImage(Image.open("./theme/neko.png").resize(ansResize)), (1323, 662), "チューリップ"]
        ]
        correctIndex = 1
        # ボタンの設定
        def answerCallback(id):
            def x():
                if (id == correctIndex):
                    self.changePage(self.correctFrame)
                else:
                    self.changePage(self.incorrectFrame)
            return x
        cntr = 0
        self.answerChoiceBtn = list()
        self.answerChoiceLabel = list()
        for im, pos, name in self.answerChoices:
            self.answerChoiceBtn.append(tk.Button(self.answerFrame, command=answerCallback(cntr), image=im))
            self.answerChoiceLabel.append(tk.Label(self.answerFrame, text=name, font=("Helvetica", "36"), fg="black", bg="light gray"))
            self.answerChoiceBtn[cntr].place(x=pos[0], y=pos[1], width=ansResize[0], height=ansResize[1])
            self.answerChoiceLabel[cntr].place(x=pos[0], y=pos[1]+ansResize[1], width=ansLabelSize[0], height=ansLabelSize[1])
            cntr += 1
        """
        # 使わなかったボタン
        self.toCheckBtn = tk.Button(self.answerFrame, text="正解へ", command=lambda: self.changePage(self.correctFrame))
        self.toCheckBtn.place(x=fW-200, y=fH-100, width=100, height=50)
        #self.toCheckBtn.pack(side=tk.BOTTOM, anchor=tk.E, ipadx=100, ipady=30, padx=20, pady=20)
        """

# correct --------------------------------------------------------------------------------------------------------------------------------
        # フレームの設定
        self.correctFrame = tk.Frame(bg="white")
        self.correctFrame.grid(row=0, column=0, sticky="nsew")
        # 画像の読み込み
        self.correctBackImage = ImageTk.PhotoImage(file="./img/correct.png")
        """
        # ラベルの設定
        self.correctLabel = tk.Label(self.correctFrame, text="正解！", font=("Helvetica", "35"), bg="gray")
        self.correctLabel.pack(anchor='center', expand=True)
        """
        # キャンバスの設定
        self.correctCanvas = tk.Canvas(self.correctFrame, bg="white")
        self.correctCanvas.create_image(hW, hH, image=self.correctBackImage)
        self.tutorialCanvas.create_text(hW, 40, text="ネコ", font=("helvetica", "48"), fill="black")
        self.answerCanvas.create_image(hW, hH, image=self.answerChoices[0][0])
        self.correctCanvas.place(x=0, y=0, width=fW, height=fH)
        """
        # 使わなかったボタン
        self.toTitleCBtn = tk.Button(self.correctFrame, text="next", command=lambda: self.changePage(self.titleFrame))
        self.toTitleCBtn.pack()
        """

# incorrect --------------------------------------------------------------------------------------------------------------------------------
        # フレームの設定
        self.incorrectFrame = tk.Frame(bg="white")
        self.incorrectFrame.grid(row=0, column=0, sticky="nsew")
        # 画像の読み込み
        self.incorrectBackImage = ImageTk.PhotoImage(file="./img/incorrect.png")
        """
        # ラベルの設定
        self.incorrectLabel = tk.Label(self.incorrectFrame, text="不正解", font=("Helvetica", "35"), bg="white")
        self.incorrectLabel.pack(anchor='center', expand=True)
        """
        # キャンバスの設定
        self.incorrectCanvas = tk.Canvas(self.incorrectFrame, bg="white")
        self.incorrectCanvas.create_image(hW, hH, image=self.incorrectBackImage)
        self.incorrectCanvas.place(x=0, y=0, width=fW, height=fH)
        """
        # 使わなかったボタン
        self.toTitleIBtn = tk.Button(self.incorrectFrame, text="next", command=lambda: self.changePage(self.titleFrame))
        self.toTitleIBtn.pack()
        """
        
        # タイトル画面を最前面にする
        self.drawingFrame.tkraise()
        
        drawingTimer(1)  # デバッグ用

    # 画面遷移する関数
    # page: 遷移先のフレーム
    def changePage(self, page):
        page.tkraise()

    # キャンバス内をキャプチャする関数
    def canvasCapture(self, c):
        """
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