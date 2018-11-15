import socket
import time
from tkinter import *

HOST = '192.168.1.3'  # The server's hostname or IP address
PORT = 60000          # The port used by the server

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))


def start_countdown():
    sock.send(b'start_timer')
    return


def start_video1():
    sock.send(b'video1')
    return


def start_video2():
    sock.send(b'video2')
    return


def show_hint(event):
    sock.send(b'help')
    entry = event.widget.master.grid_slaves(1, 1)[0]
    text = entry.get(1.0, END)
    time.sleep(1)
    print(text)
    sock.send(text.encode())
    return


def destroy_hint():
    sock.send(b'destroy_help')


def reset_timer():
    sock.send(b'reset_timer')

def activate_biohazard():
    sock.send(b'biohazard')


class ControlGui(Frame):
    def __init__(self, parent=None, **kw):
        Frame.__init__(self, parent, kw)
        self.grid()

        self.columnconfigure(0, weight=1, pad=5)
        self.columnconfigure(1, weight=1, pad=5)
        self.columnconfigure(2, weight=1, pad=5)
        self.rowconfigure(0, weight=1, pad=5)
        self.rowconfigure(1, weight=1, pad=5)
        self.rowconfigure(2, weight=1, pad=5)
        self.rowconfigure(3, weight=1, pad=5)
        self.rowconfigure(4, weight=1, pad=5)
        self.rowconfigure(5, weight=1, pad=5)

        empty = Label(self)
        empty.grid(row=0, column=0, sticky=NSEW)

        start_countdown_button = Button(self, text="Start Countdown", command=start_countdown)
        start_countdown_button.grid(row=1, column=0, sticky=NSEW)

        reset_timer_button = Button(self, text="Reset Countdown", command=reset_timer)
        reset_timer_button.grid(row=2, column=0, sticky=NSEW)

        video1_button = Button(self, text="Video MisterX 1", command=start_video1)
        video1_button.grid(row=3, column=0, sticky=NSEW)

        video2_button = Button(self, text="Video MisterX 2", command=start_video2)
        video2_button.grid(row=4, column=0, sticky=NSEW)

        biologic_hazard_button = Button(self, text="Attiva Bomba Biologica", command=activate_biohazard)
        biologic_hazard_button.grid(row=5, column=0, sticky=NSEW)

        hint_label = Label(self, text="Testo Indizio")
        hint_label.grid(row=0, column=1, columnspan=2, sticky=NSEW)

        help_entry = Text(self, width=40, height=29, font=("Arial", "15"))
        help_entry.grid(row=1, column=1, rowspan=5, columnspan=2, sticky=NSEW)

        send_help_button = Button(self, text="Invia indizio")
        send_help_button.grid(row=7, column=1, sticky=NSEW)
        send_help_button.bind("<Button-1>", show_hint)

        remove_help_button = Button(self, text="Rimuovi Indizio", command=destroy_hint)
        remove_help_button.grid(row=7, column=2, sticky=NSEW)


def main():

    root = Tk()
    cc = ControlGui(root)
    root.mainloop()


if __name__ == '__main__':
    main()


