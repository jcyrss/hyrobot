import ast
import os
from pprint import pprint
import shutil

cases_py_dir = r'cases'
cases_robot_dir = r'cases_gen'

LOG_LEVEL = 2

def myprint(level=2, *args,**kwargs):
    if level >= LOG_LEVEL:
        print(*args,**kwargs)
        
SUITE_TAGS = [
                    'force_tags',
                    'default_tags',
]

SUITE_STS = [
                    'suite_setup',
                    'suite_teardown',
]


class  SuiteFileConvert():

    def __init__(self,pyfile):


        self.pyfile = pyfile


        # 构建suite对象
        self.suite = {

            'testcases'      : []
        }


    def addOneTestCase(self, classNode):

        myprint(1,f'ClassDef: {classNode.name}')
        classname = classNode.name

        # 准备构建testcase
        testcase = {
            'classname' : classname
        }

        for level2 in classNode.body:
            # 类静态属性定义
            if type(level2) == ast.Assign:
                target = level2.targets[0]
                value = level2.value
                # myprint(f'    staticAttr: {target.id}')

                # 简单赋值语句
                if type(target) == ast.Name:

                    # 属性名 为 case_name ，表示用例名
                    if target.id == 'name' and type(value) == ast.Str:
                        testcase['name'] = value.s

                    if target.id == 'tags' and type(value) == ast.List:
                        testcase['tags'] = [elt.s for elt in value.elts]


            # 类方法定义
            elif type(level2) == ast.FunctionDef:
                myprint(1,f'    MethodDef: {level2.name}')
                if level2.name == 'setup':
                    testcase['setup'] = True
                elif level2.name == 'teardown':
                    testcase['teardown'] = True
                elif level2.name == 'teststeps':
                    testcase['teststeps'] = True

        self.suite['testcases'].append(testcase)

    def writeRobotSuiteFile(self):

        # pprint(self.suite,indent=4, width=40)

        # =============   有效性检查   ====================
        if not self.suite['testcases']:
            print('!! 没有定义测试用例 !!')
            return

        effective_testcases = []
        for tc in self.suite['testcases']:
            if 'name' not in tc:
                print(f'!! {tc["classname"]}没有 name 定义')
                continue

            if 'teststeps' not in tc:
                print(f'!! {tc["classname"]}没有 teststeps 定义')
                continue

            effective_testcases.append(tc)

        if not effective_testcases:
            return


        # ==============  写入 robot 文件   ===============

        robotFile = self.pyfile[:-3] + '.robot'
        moduleName = os.path.basename(self.pyfile)[:-3]

        settings_txt = ''
        testcases_txt = ''

        settings_txt += '''*** Settings ***\n\n'''
        settings_txt += f'Library  {moduleName}.py   WITH NAME  M\n\n'


        if 'suite_setup'  in self.suite:
            settings_txt += 'Suite Setup    M.suite_setup\n\n'

        if 'suite_teardown'  in self.suite:
            settings_txt += 'Suite Teardown    M.suite_teardown\n\n'

        if 'force_tags'  in self.suite:
            tags = '   '.join(self.suite['force_tags'])
            settings_txt += f'Force Tags     {tags}  \n\n'

        if 'default_tags'  in self.suite:
            tags = '   '.join(self.suite['default_tags'])
            settings_txt += f'Default Tags     {tags}\n\n'


        testcases_txt += '\n\n*** Test Cases ***'

        for tc in effective_testcases:
            classname = tc['classname']

            settings_txt += f'Library  {moduleName}.{classname}   WITH NAME  {classname}\n\n'

            testcases_txt += f'\n\n{tc["name"]}\n'

            if 'tags' in tc:
                tags = '   '.join(tc['tags'])
                testcases_txt += f'  [Tags]      {tags}\n'
            if 'setup' in tc:
                testcases_txt += f'  [Setup]     {classname}.setup\n'
            if 'teardown' in tc:
                testcases_txt += f'  [Teardown]  {classname}.teardown\n'

            testcases_txt += f'\n  {classname}.teststeps\n'



        with open(robotFile,'w',encoding='utf8') as rf:
            rf.write(settings_txt)
            rf.write(testcases_txt)


    def writeRobotInitFile(self):



        # ==============  写入 robot 文件   ===============

        robotFile = self.pyfile[:-3] + '.robot'
        moduleName = os.path.basename(self.pyfile)[:-3]

        settings_txt = ''
        testcases_txt = ''

        settings_txt += '''*** Settings ***\n\n'''
        settings_txt += f'Library  {moduleName}.py   WITH NAME  M\n\n'


        if 'suite_setup'  in self.suite:
            settings_txt += 'Suite Setup    M.suite_setup\n\n'

        if 'suite_teardown'  in self.suite:
            settings_txt += 'Suite Teardown    M.suite_teardown\n\n'

        if 'force_tags'  in self.suite:
            tags = '   '.join(self.suite['force_tags'])
            settings_txt += f'Force Tags     {tags}  \n\n'

        if 'default_tags'  in self.suite:
            tags = '   '.join(self.suite['default_tags'])
            settings_txt += f'Default Tags     {tags}\n\n'



        with open(robotFile,'w',encoding='utf8') as rf:
            rf.write(settings_txt)



    def handle(self):


        with open(self.pyfile, encoding='utf8') as pf:
            data = pf.read()

        # 解析 py case 代码
        tree = ast.parse(data,self.pyfile)

        for level1 in tree.body:

            # 全局变量定义
            if type(level1) == ast.Assign:
                target = level1.targets[0]
                name = target.id
                value = level1.value


                # 套件标签设置
                if name in SUITE_TAGS:
                    myprint(1,f'Assign: {name}')
                    if  type(value) == ast.List:
                        self.suite[name] = [elt.s for elt in value.elts]
                    else:
                        print(f'标签 {name} 值一定要是list类型')

            # 全局函数定义
            if type(level1) == ast.FunctionDef:
                myprint(1,f'FunctionDef: {level1.name}')

                # 套件初始化
                if level1.name in SUITE_STS:
                    self.suite[level1.name] = True

            # 类定义，对应用例
            elif type(level1) == ast.ClassDef:
                self.addOneTestCase(level1)

        if self.pyfile.endswith('__init__.py'):
            self.writeRobotInitFile()
        else:
            self.writeRobotSuiteFile()

print('''
       白月黑羽 Py2Robot  
 官网教程 http://python3.vip       

      *  *  *  *  *
      
* 用例 * Python格式 => Robot 格式 *
'''
)

import os

# 目标目录
pyFiles = []

for (dirpath, dirnames, filenames) in os.walk(cases_py_dir):
   pyFiles += [os.path.join(dirpath,fn) for fn in filenames if fn.endswith('.py')]


for file in pyFiles:
    print(f'{file}...',end='')
    sc = SuiteFileConvert(file)
    sc.handle()
    print('ok')

# print('\n\n== 产生用例执行目录 cases_robot ==')

if os.path.exists(cases_robot_dir):
    shutil.rmtree(cases_robot_dir)

shutil.copytree(cases_py_dir, cases_robot_dir)


# print(f'\n\n== 清理目录 {cases_py_dir} ==')
robotFiles = []
for (dirpath, dirnames, filenames) in os.walk(cases_py_dir):
   robotFiles += [os.path.join(dirpath,fn) for fn in filenames if fn.endswith('.robot')]

for rf in robotFiles:
    os.remove(rf)



cmd = f'robot --pythonpath . -L debug  {cases_robot_dir}'
choice= input(f'\n\n{cmd}\n按回车执行用例，按其他键退出 :')
if choice == '':
    os.system('start call ' + cmd)

