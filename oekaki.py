import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw



class App(tk.Tk):
    # コンストラクタ
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # ウィンドウに関する設定
        self.title("oekaki")
        #self.geometry("800x600")
        self.mW = self.winfo_screenwidth()
        self.hW = self.mW / 2
        self.mH = self.winfo_screenheight()
        self.hH = self.mH / 2

        # ウィンドウのグリッドを 1x1 にする
        # この処理をコメントアウトすると配置がズレる
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # フルスクリーン表示
        self.attributes("-fullscreen", True)

        # title
        self.titleFrame = tk.Frame(bg="white")
        self.titleFrame.grid(row=0, column=0, sticky="nsew")
        self.titleLabel = tk.Label(self.titleFrame, text="タイトル", font=("Helvetica", "60"), bg="white")
        self.titleLabel.pack(anchor='center', expand=True)
        self.toTutorialBtn = tk.Button(self.titleFrame, text="スタート", command=lambda: self.changePage(self.tutorialFrame))
        self.toTutorialBtn.pack(anchor=tk.N, ipadx=150, ipady=100, pady=100)
        self.exitBtn = tk.Button(self.titleFrame, text="終了", command=self.exitProc)
        self.exitBtn.pack(anchor=tk.E, padx=10, pady=10)

        # tutorial
        self.tutorialFrame = tk.Frame(bg="white")
        self.tutorialFrame.grid(row=0, column=0, sticky="nsew")
        self.toThemeBtn = tk.Button(self.tutorialFrame, text="練習を終わる", command=lambda: self.changePage(self.themeFrame))
        self.toThemeBtn.pack(side=tk.BOTTOM, ipadx=200, ipady=50)
        self.tutorialCanvas = tk.Canvas(self.tutorialFrame, bg="white")
        self.tutorialCanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.tutorialCanvas.create_text(self.hW, 50, text="練習", font=("helvetica", "60"), fill="gray")
        self.tutorialCanvas.create_text(self.hW, 120, text="まばたきで  描く・描かない  の切り替え", font=("helvetica", "30"), fill="gray")

        # theme
        self.themeFrame = tk.Frame()
        self.themeFrame.grid(row=0, column=0, sticky="nsew")
        self.themeLabel = tk.Label(self.themeFrame, text="お題提示", font=("Helvetica", "35"))
        self.themeLabel.pack(anchor='center', expand=True)
        self.toDrawingBtn = tk.Button(self.themeFrame, text="next", command=lambda: self.changePage(self.drawingFrame))
        self.toDrawingBtn.pack()

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
        #self.titleFrame.tkraise()
        self.tutorialFrame.tkraise()

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