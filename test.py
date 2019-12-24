
import sys
import pandas as pd
from pandas import Series, DataFrame
from preprocess_data import Question
# 创建问题处理对象，这样模型就可以常驻内存
que=Question()
# Restore
def enablePrint():
    sys.stdout = sys.__stdout__
enablePrint()
result=que.question_process("佛山照明的成立时间")  #东材阶级的成立时间 多输出一行“我也还不知道”
print(result)