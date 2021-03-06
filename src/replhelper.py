def jl_name(name):
    if name.endswith('_b'):
        return name[:-2] + '!'
    return name


class JuliaNameSpace(object):

    def __init__(self, julia):
        self.__julia = julia

    def __setattr__(self, name, value):
        if name.startswith('_'):
            super(JuliaNameSpace, self).__setattr__(name, value)
        else:
            setter = '''
            Main.PyCall.pyfunctionret(
                (x) -> eval(:({} = $x)),
                Any,
                PyCall.PyAny)
            '''.format(jl_name(name))
            self.__julia.eval(setter)(value)

    def __getattr__(self, name):
        if name.startswith('_'):
            return super(JuliaNameSpace, self).__getattr__(name)
        else:
            return self.__julia.eval(jl_name(name))


def ipython_options(**kwargs):
    from traitlets.config import Config
    from julia import Julia

    julia = Julia(**kwargs)
    Main = JuliaNameSpace(julia)
    user_ns = dict(
        julia=julia,
        Main=Main,
    )

    c = Config()
    c.TerminalIPythonApp.display_banner = False
    c.TerminalInteractiveShell.confirm_exit = False

    return dict(user_ns=user_ns, config=c)


def customized_ipython(**kwargs):
    import IPython
    print('')
    IPython.start_ipython(**ipython_options(**kwargs))
