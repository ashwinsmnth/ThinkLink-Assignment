
import json

import cherrypy


class RootApi(object):
    exposed = False

    def __init__(self, base_api_path: str='/video-analytics') -> None:
        self.base_api_path = base_api_path


def start(root_api=None):
    api_handlers = {}
    api_config = []
    if root_api is None:
        return start_cherrypy(api_config, api_handlers)
    root_path = getattr(root_api, "base_api_path", '/')
    api_config, api_handlers = find_apis_from_properties(root_api, root_path)
    return start_cherrypy(api_config, api_handlers)


def start_cherrypy(api_config, api_handlers):
    mount_handlers(api_config, api_handlers)
    set_cherrypy_config()
    cherrypy.server.unsubscribe()
    return cherrypy.tree


def mount_handlers(api_config, api_handlers):
    for service_name, path in api_config:
        print("Mounting handler for service {} at {}".format(service_name, path))
        api_config = {"/": {"request.dispatch": cherrypy.dispatch.MethodDispatcher()}}
        cherrypy.tree.mount(api_handlers[service_name], path, api_config)


def set_cherrypy_config():
    cherrypy.log.access_file = None
    cherrypy.log.error_file = None
    cherrypy.log.screen = False
    cherrypy.log.wsgi = False
    cherrypy.log.access_log.propagate = False
    cherrypy.log.error_log.propagate = False
    cherrypy.config.update(get_cherrypy_config())


def get_cherrypy_config():
    return {
        "error_page.404": log_message,
        "error_page.405": log_message,
        "error_page.default": log_message,
        "request.error_response": handle_error,
        "server.show_tracebacks": True,
        "request.show_tracebacks": True,
        'environment': 'embedded',
        'tools.encode.text_only': False
    }


def log_message(status, message, traceback, version):
    print("status: '{}' method: '{}' path: '{}' Message: '{}'".format(
        status, cherrypy.request.method, cherrypy.request.path_info, message))


def handle_error():
    cherrypy.response.status = 500
    exc_type, exc, trace = cherrypy._cperror._exc_info()
    cherrypy.response.body = str(exc).encode('utf-8')
    print("Exception of type {} occurred with trace: {}".format(exc_type, trace))


def find_apis_from_properties(root_api, root_path: str):
    api_handlers = {}
    api_config = []
    for name in dir(root_api):
        obj = getattr(root_api, name)
        if not getattr(obj, "exposed", False):
            continue
        api_handlers[name] = obj
        if root_path == '/':
            service_path = '/'.join(['', name])
        else:
            service_path = '/'.join([root_path, name])
        api_config.append((name, service_path))
    return api_config, api_handlers


def get_json_content():
    try:
        return json.load(cherrypy.request.body)
    except Exception as e:
        raise cherrypy.HTTPError(400, "Invalid JSON content. Exception: {0}".format(e))
