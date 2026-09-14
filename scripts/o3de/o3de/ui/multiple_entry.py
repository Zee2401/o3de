#
# Copyright (c) Contributors to the Open 3D Engine Project.
# For complete copyright and license terms please see the LICENSE at the root of this distribution.
#
# SPDX-License-Identifier: Apache-2.0 OR MIT
#
#

import tkinter as tk
from tkinter import filedialog


class _ToolTip:
    """
    A simple, robust hover tooltip for Tkinter widgets.
    """
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.id = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)
        self.widget.bind("<ButtonPress>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return
        def display():
            if not self.widget.winfo_exists():
                return
            x = self.widget.winfo_rootx() + 25
            y = self.widget.winfo_rooty() + 20
            self.tip_window = tw = tk.Toplevel(self.widget)
            tw.wm_overrideredirect(True)
            tw.wm_geometry(f"+{x}+{y}")
            label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                             background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                             font=("tahoma", "8", "normal"))
            label.pack(ipadx=1)
        self.id = self.widget.after(500, display)

    def hide_tip(self, event=None):
        if self.id:
            try:
                self.widget.after_cancel(self.id)
            except Exception:
                pass
            self.id = None
        tw = self.tip_window
        self.tip_window = None
        if tw:
            try:
                tw.destroy()
            except Exception:
                pass


class Dialog(object):
    """
    Dialog to handle the selection of names
    """

    def __init__(self, parent, input_value):

        root = self.root = tk.Toplevel(parent)
        root.title('Configure Files')
        root.resizable(True,True)

        px = parent.winfo_rootx()
        py = parent.winfo_rooty()
        root.geometry(f'400x200+{px}+{py}')

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self._main_frame = tk.Frame(self.root, borderwidth=2, relief=tk.SOLID)
        self._main_frame.columnconfigure(0, weight=1)
        self._main_frame.rowconfigure(0, weight=1)
        self._main_frame.grid(padx=8, pady=8, sticky=tk.NSEW)

        self.input_value = input_value

        if input_value:
            items = [ti.strip() for ti in input_value.split(";")]
            sanitized_items = []
            for item in items:
                if item is not None and len(item.strip())>0:
                    sanitized_items.append(item)

            text_entries = "\n".join(sanitized_items)
        else:
            text_entries = ""

        self._entry = tk.Text(self._main_frame, )
        self._entry.insert(tk.END,text_entries)
        self._entry.grid(sticky=tk.NSEW)

        button_frame = tk.Frame(self._main_frame, borderwidth=0)
        button_frame.columnconfigure(0, weight=0)
        button_frame.rowconfigure(0, weight=0)
        button_frame.rowconfigure(1, weight=0)
        button_frame.grid()

        button_add = tk.Button(button_frame, text="Ok", width=4, command=self._on_ok, underline=0)
        button_add.grid(row=0, column=0, sticky=tk.E)
        _ToolTip(button_add, "Save items and close dialog (Alt+O)")

        button_remove = tk.Button(button_frame, text="Cancel", width=4, command=self._on_cancel, underline=0)
        button_remove.grid(row=0, column=1, sticky=tk.E)
        _ToolTip(button_remove, "Cancel and close dialog (Alt+C, Esc)")

        root.bind("<Escape>", lambda event: self._on_cancel())
        root.protocol("WM_DELETE_WINDOW", self._on_cancel)

        root.bind("<Alt-o>", lambda event: self._on_ok())
        root.bind("<Alt-O>", lambda event: self._on_ok())
        root.bind("<Alt-c>", lambda event: self._on_cancel())
        root.bind("<Alt-C>", lambda event: self._on_cancel())

        root.grid()

    def _on_ok(self):
        result_string = self._entry.get("1.0", tk.END)
        result_items = [rs.strip() for rs in result_string.split("\n")]
        sanitized_items = set()
        for result_item in result_items:
            if result_item is not None and len(result_item.strip()) > 0:
                sanitized_items.add(result_item)
        self.input_value = ';'.join(sanitized_items)
        self.root.destroy()

    def _on_cancel(self):
        self.root.destroy()

    def get_result(self):
        self.root.grab_set()
        self.root.wait_window()
        return self.input_value
