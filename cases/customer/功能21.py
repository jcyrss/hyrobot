def add_order(name):
    return {
            'ret': 0,
            'info': {
                'id': 100,
                'name': name
            }
        }

def rename_order(oid):
    return {'ret': 0}

def delete_order(oid):
    return {'ret': 0}


default_tags = ['优先级7']

force_tags = ['冒烟测试','订单功能']

# 套件初始化，只执行一次
def suite_setup():
    pass

# 套件清除，只执行一次
def suite_teardown():
    pass


# 用例缺省初始化，用例本身没有初始化的时候使用这个初始化
def test_setup():
    pass

# 用例缺省清除，用例本身没有清除的时候使用这个清除
def test_teardown():
    pass

# 用例对应的类名，建议对应用例编号
class c00101:
    # 用例名，必填。 建议后面加上编号
    name = '添加订单 - 00101'
    
    # 用例标签，可选   
    tags = ['本次不测','now']

    def setup(self):
        ret = add_order('order name')

        # we could compare complicated data object easily,
        # but in Robot, that's hard
        assert ret == {
            'ret': 0,
            'info': {
                'id': 100,
                'name': 'order name'
            }
        }
        self.orderid = ret['info']['id']

    def teardown(self):
        delete_order(self.orderid)

    # 测试用例 具体操作步骤
    def teststeps(self):
        # we could easily get data "orderid" from test setup
        ret1 = rename_order(self.orderid)

        assert ret1 == {'ret': 0}




class c00102:
    name = '添加订单 - 00102'


    def teststeps(self):
        pass

    def teardown(self):
        delete_order(1)