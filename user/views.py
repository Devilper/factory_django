from django.conf import settings
import json


class InitPermission:

    def __init__(self, user):
        self.user = user
        self.permissions_dict = {}
        self.menus_dict = {}

    def init_data(self):
        """
        从数据库中获取权限信息以及用户信息
        :return:
        """
        self.permissions_queryset = self.user.roles.filter(permissions__url__isnull=False).order_by(
            "permissions__parent_id").values(
            'permissions__id',
            'permissions__url',
            'permissions__title',
            'permissions__parent_id',
        )

        return self.permissions_queryset

    def init_permissions_dict(self):
        """
            初始化权限，获取当前用户权限并添加到session中
        将当前用户权限信息转换为以下格式，并将其添加到Session中
        {
            '/index.html': ['GET','POST','DEL','EDIT],
            '/detail-(\d+).html': ['GET','POST','DEL','EDIT],
        }
        :return:
        """

        for row in self.init_data():
            if row["permissions__url"] in self.permissions_dict:
                self.permissions_dict[row["permissions__url"]].append(row["permissions__action__code"])
            else:
                self.permissions_dict[row["permissions__url"]] = [row["permissions__action__code"], ]
        print('init', self.permissions_dict)

        return self.permissions_dict

    def init_menus_dict(self):
        """
               self.menus_dict={
               1:{
               title:'客户管理',icon:'fa fa-coffe',children:[
               {'id':1,'url':'/customer/list/','title':'客户列表'}
               ...
               ]
               }
               }
               :return:
        """
        for row in self.init_data():
            if row['permissions__parent_id']:
                self.menus_dict[row["permissions__parent_id"]]["children"].append(
                    {
                        'id': row['permissions__id'],
                        'title': row['permissions__title'],
                        'url': row['permissions__url']

                    }
                )
            else:
                self.menus_dict[row["permissions__id"]] = {
                            'id': row['permissions__id'],
                            'title': row['permissions__title'],
                            'url': row['permissions__url'],
                            "children": [
                            ]
                        }

        return self.menus_dict

