from breezy.commands import plugin_cmds

plugin_cmds.register_lazy('cmd_wikkid', ['wiki'],
                          'breezy.plugins.wikkid.commands')
