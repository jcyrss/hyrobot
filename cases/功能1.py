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

def suite_setup():
    pass

def suite_teardown():
    pass


class case000001:
    name = '添加订单 - tc000001'
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

    def teststeps(self):
        # we could easily get data "orderid" from test setup
        ret1 = rename_order(self.orderid)

        assert ret1 == {'ret': 0}

    def teardown(self):
        delete_order(self.orderid)



class case000002:
    name = '添加订单 - tc000002'

    def setup(self):
        ret = add_order('order name')

        # we could compare complicated data object easily,
        # but in Robot, that's hard
        assert ret == {
            'ret' : 0,
            'info' : {
                'id': 100,
                'name': 'order name'
            }
        }
        self.orderid = ret['info']['id']

    def teststeps(self):
        # we could easily get data "orderid" from test setup
        ret1 = rename_order(self.orderid)

        assert (ret1 == {'ret' : 0})

    def teardown(self):
        delete_order(self.orderid)