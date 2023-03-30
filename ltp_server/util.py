

def resultSuccess(result, message='ok'):
    return {
        'code': 0,
        'result': result,
        'message': message,
        'type': 'success',
    }


def resultError(message='Request failed'):
    return {
        'code': -1,
        'result': '',
        'message': message,
        'type': 'success',
    }


def menu_config():
    return {
        'path': '/dashboard',
        'name': 'Dashboard',
        'component': 'LAYOUT',
        'redirect': '/dashboard/analysis',
        'meta': {
            'title': 'routes.dashboard.dashboard',
            'hideChildrenInMenu': 'true',
            'icon': 'bx:bx-home',
        },
        'children': [
            {
                'path': 'analysis',
                'name': 'Analysis',
                'component': '/dashboard/analysis/index',
                'meta': {
                    'hideMenu': 'true',
                    'hideBreadcrumb': 'true',
                    'title': 'routes.dashboard.analysis',
                    'currentActiveMenu': '/dashboard',
                    'icon': 'bx:bx-home',
                },
            },
            {
                'path': 'workbench',
                'name': 'Workbench',
                'component': '/dashboard/workbench/index',
                'meta': {
                    'hideMenu': 'true',
                    'hideBreadcrumb': 'true',
                    'title': 'routes.dashboard.workbench',
                    'currentActiveMenu': '/dashboard',
                    'icon': 'bx:bx-home',
                },
            },
        ],
    }
