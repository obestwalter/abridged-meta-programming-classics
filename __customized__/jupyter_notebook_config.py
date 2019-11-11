c.JupyterApp.answer_yes = True
c.NotebookApp.token = ''
c.NotebookApp.allow_origin = '*'  #allow all origins
c.NotebookApp.ip = '0.0.0.0'  # listen on all IPs
c.ContentsManager.hide_globs = [
    '__scratchpad.*',
    '__000__.md',
    '__pycache__',
    '*.pyc',
    '*.pyo',
    '.DS_Store',
    '*.so',
    '*.dylib',
    '*~',
]
