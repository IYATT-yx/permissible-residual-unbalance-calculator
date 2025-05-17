from calculator import Calculator

import tkinter as tk
import webbrowser
import buildtime
from tkinter import messagebox

class Main(tk.Frame):
    SPEED = 0
    """计算选项：速度"""
    PERMISSIBLERESIDUALUNBALANCE = 1
    """计算选项：许用剩余不平衡量"""
    QUALITYGRADES = 2
    """计算选项：品质等级"""

    # 许用剩余不平衡量单位
    GMM = 'g·mm 克·毫米'
    G = 'g 克'    

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()

    def create(self):
        tk.Label(self, text='转子质量：').grid(row=0, column=0, sticky=tk.W)
        tk.Label(self, text='转速：').grid(row=1, column=0, sticky=tk.W)
        tk.Label(self, text='许用剩余不平衡量：').grid(row=2, column=0, sticky=tk.W)
        tk.Label(self, text='品质等级 G：').grid(row=3, column=0, sticky=tk.W)
        tk.Label(self, text='校正半径').grid(row=4, column=0, sticky=tk.W)
        tk.Label(self, text='计算项目：').grid(row=5, column=0, sticky=tk.W)
        tk.Label(self, text='单位：').grid(row=6, column=0, sticky=tk.W)

        self.rotorMassValue = tk.DoubleVar()
        """转子质量"""
        self.speedValue = tk.DoubleVar()
        """转速"""
        self.permissibleResidualUnbalanceValue = tk.DoubleVar()
        """许用剩余不平衡量"""
        self.qualityGradesValue = tk.DoubleVar()
        """品质等级"""
        self.correctionRadiusValue = tk.DoubleVar()

        tk.Entry(self, textvariable=self.rotorMassValue).grid(row=0, column=1, sticky=tk.EW)
        self.speedEntry = tk.Entry(self, textvariable=self.speedValue)
        self.speedEntry.grid(row=1, column=1, sticky=tk.EW)
        self.permissibleResidualUnbalanceEntry = tk.Entry(self, textvariable=self.permissibleResidualUnbalanceValue)
        self.permissibleResidualUnbalanceEntry.grid(row=2, column=1, sticky=tk.EW)
        self.qualityGradesEntry = tk.Entry(self, textvariable=self.qualityGradesValue)
        self.qualityGradesEntry.grid(row=3, column=1, sticky=tk.EW)
        self.correctionRadiusEntry = tk.Entry(self, textvariable=self.correctionRadiusValue)
        self.correctionRadiusEntry.grid(row=4, column=1, sticky=tk.EW)

        self.unit = tk.StringVar()
        self.unit.set(Main.GMM) # 默认：克·毫米
        tk.Label(self, text='kg 千克').grid(row=0, column=2, sticky=tk.W)
        tk.Label(self, text='rpm 转/分钟').grid(row=1, column=2, sticky=tk.W)
        tk.Label(self, textvariable=self.unit).grid(row=2, column=2, sticky=tk.W)
        tk.Button(self, text='参考品质等级', command=self.onOpenQualityGrades).grid(row=3, column=2, sticky=tk.EW)
        tk.Label(self, text='mm 毫米').grid(row=4, column=2, sticky=tk.W)

        self.calculatorOptions = tk.IntVar()
        tk.Radiobutton(self, text='计算转速', variable=self.calculatorOptions, value=self.SPEED, command=self.onCalculatorOptionChanged) \
        .grid(row=5, column=1, sticky=tk.W)
        tk.Radiobutton(self, text='计算许用剩余不平衡量', variable=self.calculatorOptions, value=self.PERMISSIBLERESIDUALUNBALANCE, command=self.onCalculatorOptionChanged) \
        .grid(row=5, column=2, sticky=tk.W)
        tk.Radiobutton(self, text='计算品质等级', variable=self.calculatorOptions, value=self.QUALITYGRADES, command=self.onCalculatorOptionChanged) \
        .grid(row=5, column=3, sticky=tk.W)
        self.calculatorOptions.set(self.PERMISSIBLERESIDUALUNBALANCE)
        self.onCalculatorOptionChanged()

        tk.Radiobutton(self, text=Main.GMM, variable=self.unit, value=Main.GMM, command=self.onUnitOptionChanged).grid(row=6, column=1, sticky=tk.W)
        tk.Radiobutton(self, text=Main.G, variable=self.unit, value=Main.G, command=self.onUnitOptionChanged).grid(row=6, column=2, sticky=tk.W)
        self.onUnitOptionChanged()
        
        tk.Button(self, text='计算', bd=3, command=self.calculate).grid(row=0, column=3, rowspan=5, sticky=tk.NSEW)

        tk.Label(self, text='计算依据：GB/T 9239.1-2006 机械振动 恒态（刚性）转子平衡品质要求 第1部分：规范与平衡允差的检验').grid(row=7, column=0, columnspan=4, sticky=tk.EW)
        tk.Label(self, text=f'IYATT-yx iyatt@iyatt.com {buildtime.buildTime}').grid(row=8, column=0, columnspan=5, sticky=tk.W)
    
    def onOpenQualityGrades(self):
        webbrowser.open('https://blog.iyatt.com/?p=20102#%E6%81%92%E6%80%81%EF%BC%88%E5%88%9A%E6%80%A7%EF%BC%89%E8%BD%AC%E5%AD%90%E5%B9%B3%E8%A1%A1%E5%93%81%E8%B4%A8%E5%88%86%E7%BA%A7%E6%8C%87%E5%8D%97%E3%80%90G_%E5%8F%96%E5%80%BC%E3%80%91')

    def onCalculatorOptionChanged(self):
        """计算选项改变事件
        """
        match(self.calculatorOptions.get()):
            case self.SPEED:
                self.speedEntry.config(state=tk.DISABLED, border=5)
                self.permissibleResidualUnbalanceEntry.config(state=tk.NORMAL, border=1)
                self.qualityGradesEntry.config(state=tk.NORMAL, border=1)
            case self.PERMISSIBLERESIDUALUNBALANCE:
                self.speedEntry.config(state=tk.NORMAL, border=1)
                self.permissibleResidualUnbalanceEntry.config(state=tk.DISABLED, border=5)
                self.qualityGradesEntry.config(state=tk.NORMAL, border=1)
            case self.QUALITYGRADES:
                self.speedEntry.config(state=tk.NORMAL, border=1)
                self.permissibleResidualUnbalanceEntry.config(state=tk.NORMAL, border=1)
                self.qualityGradesEntry.config(state=tk.DISABLED, border=5)

    def onUnitOptionChanged(self):
        """单位选项改变事件
        """
        match(self.unit.get()):
            case Main.GMM:
                self.correctionRadiusEntry.config(state=tk.DISABLED)
            case Main.G:
                self.correctionRadiusEntry.config(state=tk.NORMAL)
    
    def calculate(self):
        try:
            unit = self.unit.get()
            match(self.calculatorOptions.get()):
                case self.PERMISSIBLERESIDUALUNBALANCE:
                    if unit == Main.GMM:
                        self.permissibleResidualUnbalanceValue.set(
                            Calculator.calcPermissibleResidualUnbalance(
                                self.rotorMassValue.get(),
                                self.speedValue.get(),
                                self.qualityGradesValue.get(),
                            )
                        )
                    else:
                        self.permissibleResidualUnbalanceValue.set(
                            Calculator.calcPermissibleResidualUnbalance(
                                self.rotorMassValue.get(),
                                self.speedValue.get(),
                                self.qualityGradesValue.get(),
                                self.correctionRadiusValue.get()
                            )
                        )
                case self.SPEED:
                    if unit == Main.GMM:
                        self.speedValue.set(
                            Calculator.calcSpeed(
                                self.rotorMassValue.get(),
                                self.qualityGradesValue.get(),
                                self.permissibleResidualUnbalanceValue.get(),
                                'gmm'
                            )
                        )
                    else:
                        self.speedValue.set(
                            Calculator.calcSpeed(
                                self.rotorMassValue.get(),
                                self.qualityGradesValue.get(),
                                self.permissibleResidualUnbalanceValue.get(),
                                'g',
                                self.correctionRadiusValue.get()
                            )
                        )
                case self.QUALITYGRADES:
                    if unit == Main.GMM:
                        self.qualityGradesValue.set(
                            Calculator.calcQualityGrades(
                                self.rotorMassValue.get(),
                                self.speedValue.get(),
                                self.permissibleResidualUnbalanceValue.get(),
                                'gmm'
                            )
                        )
                    else:
                        self.qualityGradesValue.set(
                            Calculator.calcQualityGrades(
                                self.rotorMassValue.get(),
                                self.speedValue.get(),
                                self.permissibleResidualUnbalanceValue.get(),
                                'g',
                                self.correctionRadiusValue.get()
                            )
                        )

        except Exception as e:
            messagebox.showerror('错误', str(e))
