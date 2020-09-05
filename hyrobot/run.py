import os,sys,pprint

print('\n根据环境变量Path，使用python解释器: %s\n' % sys.executable)

if sys.version_info.major is not 3:
    print("黑羽robot只支持 Python 3.7、3.8 版本")
    exit()

if sys.version_info.minor  not in [7,8]:
    print("黑羽robot只支持 Python 3.7、3.8 版本")
    exit()

from hyrobot.core import reportHan,convert2RF,runRF,clearRobotFile

def main():

    # 运行结果存入字典
    result = {}

    # 只清除所有robot用例文件
    if '--delrf' in sys.argv:
        clearRobotFile()
        exit(0)

    # 只转化Python用例为robotframework格式用例
    if '--torf' in sys.argv:
        convert2RF()
        exit(0)

    # 只运行测试
    if '--runrf' in sys.argv:
        runRF()
        exit(0)        

    # 只汉化测试报告
    if '--hanrf' in sys.argv:
        reportHan()
        exit(0)


    # 所有步骤都执行
    convert2RF()

    ret = runRF()    
    print(f'-------- RF execute result code: {ret} --------')
    result['run_robot'] = ret

    # 如果运行成功，执行汉化
    if ret < 5: # 0 success, 1 faiure, 252 no matches found
        reportHan()
        os.system('log.html')

    return result

if __name__ == '__main__':
    result = main()