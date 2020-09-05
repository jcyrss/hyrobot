from robot.libraries.BuiltIn import logger
from robot.libraries.BuiltIn import BuiltIn

# 存储 robotframework BuiltIn实例对象
# 通过它可以调用任意 内置关键字对应的函数
# 比如 
# from hyrobot.common import RFB
# RFB.fail('直接报告测试错误')
RFB = BuiltIn()

# 存储 全局共享 数据
GSTORE = {}

def INFO(info):
    """
    在运行终端和测试报告中打印 重要信息，
    使得 运行报告更加清晰

    参数：
    info :   信息描述
    """
    logger.info(f'{info}',True,True)

def STEP(stepNo,desc):
    """
    在运行终端和测试报告中打印出 测试步骤说明，
    使得 运行报告更加清晰

    参数：
    stepNo : 指定 是第几步
    desc :   步骤描述
    """
    logger.info(f'\n-- 第 {stepNo} 步 -- {desc} \n',True,True)


def CHECK_POINT(desc, condition):
    """
    检查点

    参数：
    desc :   检查点文字描述
    condition ： 检查点 表达式
    """
    logger.info(f'\n** 检查点 **  {desc} ',True,True)

    if condition:
        logger.info('---->  通过\n',True,True)
    else:
        logger.info('---->   !! 不通过!!\n',True,True)
        raise AssertionError(f'\n** 检查点不通过 **  {desc} ' )



# def CHECK_POINT2(desc, conditionRet):
#     print(f'\n\033[34m** 检查点 **  {desc} \033[0m')
#
#     if conditionRet:
#         print('\033[32m---->  通过 \033[0m')
#     else:
#         print('\033[31m---->   !! 不通过!! \033[0m')
#         raise AssertionError(f'\n** 检查点不通过 **  {desc} ' )