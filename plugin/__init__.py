from bzrlib.commands import plugin_cmds

plugin_cmds.register_lazy('cmd_wikkid', ['wiki'],
                          'bzrlib.plugins.wikkid.commands')
