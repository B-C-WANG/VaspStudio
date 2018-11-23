
from PyQt5.QtGui import QColor

class XVI_Status():
    Submitted = "Submitted"
    NotSubmitted = "Not_Submit"
    Canceled = "Canceled"

    Finished = "Finished_And_Linked"

    Convergence = "Convergence"
    NotConvergence  = "Not_Convergence"

    FreqPass = "Freq_Check_Pass"
    FreqFail = "Freq_Check_Fail"

class Status():

    INFO = "Info_qwe"
    WARN = "Warn_qwe"
    ERROR = "Error_qwe"
    PASS = "Pass_qwe"
    FAILED = "Failed_qwe"

class Type():

    Origin = "Artificial Structure" # 人为摆出的结构
    Convergence = "Convergence - VASP Opted Structure" #VASP优化过后的结构
    NotConvergence = "Not Convergence - VASP Opted Structure"

Type_Color = {

    Type.Origin: QColor(128,138,135),  # 灰色
    Type.Convergence: QColor(	127,255,212	), # 青色
    Type.NotConvergence:QColor(255,0,0)    # 橘色
}

STATUS_COLOR = {
    XVI_Status.Submitted:QColor(255,255,0), # 黄色
    XVI_Status.NotSubmitted:QColor(128,138,135), # 灰色
    XVI_Status.Finished:QColor(255,165,0), # 翠绿色
    XVI_Status.Convergence:QColor(0,255,255), # 蓝色
    XVI_Status.NotConvergence:QColor(255,0,0), # 红色
    XVI_Status.Canceled:QColor(128,138,135),
    XVI_Status.FreqFail:QColor(210,105,30), # 棕色
    XVI_Status.FreqPass:QColor(0,255,0) # 绿色

}


class Checker():
    # VASPStu的函数全部返回Checker，Checker被Main调用，得到output，只有PASS状态才能得到结果
    # 返回值：如果status为Failed，就返回Failed，否则返回output，采用output调用
    '''

    使用例子：在Main中使用check包装一下
    check(Checker(status=FAILED,window_status=Error,window_string="Error"))

    check(Checker(status=Pass,output="123"))

    check(Checker(status=Pass,output="123",windows_status=Warn,window_string="Attention"))



    '''
    def __init__(self,status,output=None,window_status=None,window_string=None):

        self.status = status # 返回状态，Pass 或 Failed
        assert self.status in [Status.PASS,Status.FAILED]
        self.window_status = window_status # window状态，Info Warn Error等
        if window_status != None:
            assert  self.window_status in [Status.WARN,Status.INFO,Status.ERROR]
        if self.window_status is not None:
            assert window_status is not None
        self.window_string = window_string
        # 返回值，如果status为Failed，强制output为None
        self.output_ = output if Status != Status.FAILED else Status.PASS

