import urwid
from urwid import CENTER
import time

from chat.commands import CommandDispatcher


class _PatchedEdit(urwid.Edit):
    _metaclass_ = urwid.signals.MetaSignals
    signals = ['command_entered']

    def keypress(self, size, key):
        if key == 'enter':
            urwid.emit_signal(
                self, 'command_entered', self, self.get_edit_text())
            super().set_edit_text('')
            return
        elif key == 'esc':
            super().set_edit_text('')
            return
        urwid.Edit.keypress(self, size, key)


class ChatInterface(object):
    def __init__(self):
        self._messages = []
        self._connected_clients = []
        self._main_loop = urwid.MainLoop(self._init_interface())
        self._cmd_dispatcher = CommandDispatcher(self)

    def _init_interface(self):
        """Returns main interface frame."""
        header = urwid.LineBox(
            urwid.Text('Local Chat by Yury Zaitsau, 2017', align=CENTER))
        body = urwid.Columns([
            (urwid.LineBox(urwid.ListBox(self._messages), title="Chat history")),
            ('fixed', 20, urwid.LineBox(urwid.ListBox(self._connected_clients), title="Clients online")),
        ])
        edit = _PatchedEdit(caption=' command: ', multiline=True)
        urwid.connect_signal(edit, 'command_entered', self._command_entered)
        footer = urwid.LineBox(edit, title='Command line')
        frame = urwid.Frame(body, header, footer)
        frame.focus_position = 'footer'
        return frame

    def _command_entered(self, edit, text):
        if not text.startswith('\\'):
            text = '\msg ' + text
        text = text[1:]
        self._cmd_dispatcher.onecmd(text)

    def run(self):
        try:
            self._main_loop.run()
        except KeyboardInterrupt:
            self._stop_program_logics()

    def stop(self):
        self._stop_program_logics()
        self._stop_main_loop()

    def _stop_program_logics(self):
        pass

    def _stop_main_loop(self, *args, **kwargs):
        raise urwid.ExitMainLoop()

    def add_message(self, source, message):
        cur_time = time.strftime('%H:%M:%S')
        text = '%16s %s ==> %s\n' % (source, cur_time, message)
        self._messages.insert(0, urwid.Text(text))

    def add_client(self, client):
        text = ' %s' % client
        self._connected_clients.append(urwid.Text(text))

    def remove_client(self, client):
        try:
            self._connected_clients.remove(client)
        except ValueError:
            pass
