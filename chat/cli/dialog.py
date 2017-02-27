import urwid


class DialogExit(Exception):
    pass


class Dialog:
    _palette = [
        ('body', 'black', 'light gray', 'standout'),
        ('border', 'black', 'dark blue'),
        ('shadow', 'white', 'black'),
        ('selectable', 'black', 'dark cyan'),
        ('focus', 'white', 'dark blue', 'bold'),
        ('focustext', 'light gray', 'dark blue'),
    ]

    def __init__(self, text, height, width, body=None):
        width = int(width)
        if width <= 0:
            width = ('relative', 80)
        height = int(height)
        if height <= 0:
            height = ('relative', 80)

        self.body = body
        if body is None:
            # fill space with nothing
            body = urwid.Filler(urwid.Divider(), 'top')

        self.frame = urwid.Frame(body, focus_part='footer')
        if text is not None:
            self.frame.header = urwid.Pile(
                [urwid.Text(text), urwid.Divider()])
        w = self.frame

        # pad area around listbox
        w = urwid.Padding(w, ('fixed left', 2), ('fixed right', 2))
        w = urwid.Filler(w, ('fixed top', 1), ('fixed bottom', 1))
        w = urwid.AttrWrap(w, 'body')

        # "shadow" effect
        w = urwid.Columns([w, ('fixed', 2, urwid.AttrWrap(
            urwid.Filler(urwid.Text(('border', '  ')), "top"), 'shadow'))])
        w = urwid.Frame(
            w, footer=urwid.AttrWrap(urwid.Text(('border', '  ')), 'shadow'))

        # outermost border area
        w = urwid.Padding(w, 'center', width)
        w = urwid.Filler(w, 'middle', height)
        w = urwid.AttrWrap(w, 'border')

        self.view = w

    def add_buttons(self, buttons):
        l = []
        for name, exitcode in buttons:
            b = urwid.Button(name, self._button_press)
            b.exitcode = exitcode
            b = urwid.AttrWrap(b, 'selectable', 'focus')
            l.append(b)
        self.buttons = urwid.GridFlow(l, 10, 3, 1, 'center')
        self.frame.footer = urwid.Pile(
            [urwid.Divider(), self.buttons], focus_item=1)

    def _button_press(self, button):
        raise DialogExit(button.exitcode)

    def show(self):
        self.loop = urwid.MainLoop(self.view, self._palette)
        try:
            self.loop.run()
        except DialogExit as e:
            return self._on_exit(e.args[0])
        except KeyboardInterrupt:
            return (1, '')

    def _on_exit(self, exitcode):
        return exitcode, ""


class CheckListDialog(Dialog):
    def __init__(self, text, height, width, items):
        radio_group = []
        l = []
        self.items = []
        for tag in items:
            if len(self.items) == 0:
                w = urwid.RadioButton(radio_group, tag, True)
            else:
                w = urwid.RadioButton(radio_group, tag, False)
            self.items.append(w)
            w = urwid.AttrWrap(w, 'selectable', 'focus')
            l.append(w)

        lb = urwid.ListBox(l)
        lb = urwid.AttrWrap(lb, "selectable")
        Dialog.__init__(self, text, height, width, lb)

        self.frame.set_focus('body')
        self.add_buttons([("OK", 0), ("Cancel", 1)])

    def unhandled_key(self, size, k):
        if k in ('up', 'page up'):
            self.frame.set_focus('body')
        if k in ('down', 'page down'):
            self.frame.set_focus('footer')
        if k == 'enter':
            # pass enter to the "ok" button
            self.frame.set_focus('footer')
            self.buttons.set_focus(0)
            self.view.keypress(size, k)

    def _on_exit(self, exitcode):
        """Print the tag of the item selected."""
        if exitcode != 0:
            return exitcode, ""
        s = ""
        for i in self.items:
            if i.get_state():
                s = i.get_label()
                break
        return exitcode, s
