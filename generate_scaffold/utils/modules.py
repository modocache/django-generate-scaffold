def import_child(module_name):
    module = __import__(module_name)
    for layer in module_name.split('.')[1:]:
        module = getattr(module, layer)
    return module
