def initial_session(user, request):
    """
    用来初始化session以及获取注册权限

    """

    # 注册用户的权限 ###################################################################################################

    permissions = user.roles.all().values("permissions__url", "permissions__group_id", "permissions__action").distinct()
    print("permissions", permissions)

    permission_dict = {}
    for item in permissions:
        gid = item.get('permissions__group_id')

        if not gid in permission_dict:

            permission_dict[gid] = {
                "urls": [item["permissions__url"], ],
                "actions": [item["permissions__action"], ]
            }
        else:
            permission_dict[gid]["urls"].append(item["permissions__url"])
            permission_dict[gid]["actions"].append(item["permissions__action"])

    print(permission_dict)
    request.session['permission_dict'] = permission_dict

    # 注册菜单权限 ###################################################################################################

    permissions = user.roles.all().values("permissions__url", "permissions__action",
                                          "permissions__group__title").distinct()

    print("-------->permissions", permissions)

    menu_permission_list = []
    for item in permissions:
        if item["permissions__action"] == "list":
            menu_permission_list.append((item["permissions__url"], item["permissions__group__title"]))


    print("--------->menu_permission_list", menu_permission_list)

    request.session["menu_permission_list"] = menu_permission_list


#  操作内容过程
'''
[{'permissions__url': '/users/',
  'permissions__group_id': 1,
  'permissions__action': 'list'},

 {'permissions__url': '/users/add/',
  'permissions__group_id': 1,
  'permissions__action': 'add'},

 {'permissions__url': '/users/delete/(\\d+)',
  'permissions__group_id': 1,
  'permissions__action': 'delete'},

 {'permissions__url': 'users/edit/(\\d+)',
  'permissions__group_id': 1,
  'permissions__action': 'edit'},

 {'permissions__url': '/roles/',
  'permissions__group_id': 2,
  'permissions__action': 'list'}

 ]

{
    1: {
        "urls": ['/users/', '/users/add/', '/users/delete/(\\d+)', 'users/edit/(\\d+)']
        "actions": ['list', "add", 'delete', 'edit']
    },

    2: {
        "urls": ['/roles/']
        "actions": ['list']
    }
}
'''

'''

      permissions = user.roles.all().values("permissions__url").distinct()

     permission_list = []

     for item in permissions:

         permission_list.append(item["permissions__url"])

     print(permission_list)

     request.session["permission_list"] = permission_list

    '''
