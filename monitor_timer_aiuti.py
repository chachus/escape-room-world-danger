from tkinter import *
import simpleaudio as sa
import time
import threading
import random
import queue
import socket
import select
import os
import subprocess

HOST = "192.168.1.3"
PORT = 60000

codes = ["AF369HYUZ", "DW327KOLI", "KU789MNIL", "ST672FRGH", "WS741ESFG", "SW309LIJU"]

count = 0

hint_sound = sa.WaveObject.from_wave_file("./files/hint_sound.wav")
wrong_sound = sa.WaveObject.from_wave_file("./files/wrong_buzzer.wav")
deactivate_sound = sa.WaveObject.from_wave_file("./files/shut_down.wav")
red_alert = sa.WaveObject.from_wave_file("./files/red_alert.wav")

def recv_timeout(socket, timeout=2):
        total_data = []
        data=b''
        
        begin = time.time()
        while True:
            if total_data and time.time()-begin > timeout:
                break
            elif time.time()-begin > timeout*2:
                break
            
            try:
                data = socket.recv(4096)
                if data:
                    total_data.append(data)
                    begin = time.time()
                else:
                    time.sleep(0.1)
            except:
                pass
        return total_data

def check_code(event, entry_code):
    global count
    text = event.widget.get()
    if text == codes[entry_code]:
        event.widget.config(state=DISABLED)
        event.widget.unbind("<Return>")
        deactivate_sound.play()
        count = count + 1
    else:
        event.widget.delete(0, END)
        wrong_sound.play()
        event.widget.master.master.focus_set()
        
    if count == 6:
        event.widget.master.grid_slaves(0, 0)[0].config(text="BOMBA BIOLOGICA DISATTIVATA", fg="green")
        event.widget.after(5000, event.widget.master.master.destroy)

class GUI(Frame):
    # Set up the GUI
    # Add more GUI stuff here
    def __init__(self, parent, queue, **kw):
        Frame.__init__(self, parent, kw)
        self.queue = queue
        self.start_time = 0.0
        self.elapsed_time = 0.0
        self.running = 0
        self.is_game_over = True
        self.hint_window = None # first inizialisation for auto-removal
        self.time_str = StringVar()
        self.make_countdown()

    def make_countdown(self):
        time_label = Label(self, bg="black", fg="red", font=("DS-Digital", "350"), textvariable=self.time_str)
        self.set_time(self.elapsed_time)
        time_label.pack(fill=BOTH, expand=1)

    def update_time(self):
        """ Update the label with elapsed time. """
        self.elapsed_time = time.time() - self.start_time
        self.set_time(self.elapsed_time)
        self._timer = self.after(50, self.update_time)

    def set_time(self, elap):
        minutes = int(elap / 60)
        c_minutes = int(60 - (elap / 60))
        #seconds = int(elap - minutes * 60.0)
        c_seconds = int(60 - (elap - minutes * 60.0))
        if c_minutes == 0 and c_seconds == 0 and self.is_game_over:
            self.is_game_over = False
            self.game_over()
        if c_seconds == 60:
            c_seconds = 00
        #hseconds = int((elap - minutes * 60.0 - seconds) * 100)
        self.time_str.set('%02d:%02d' % (c_minutes, c_seconds))

    def start_countdown(self):
        """ Start the stopwatch """
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.update_time()
            self.running = 1
            
    def stop_countdown(self):
        """ Stop the stopwatch, ignore if stopped. """
        if self.running:
            self.after_cancel(self._timer)
            self.elapsed_time = time.time() - self.start_time
            self.set_time(self.elapsed_time)
            self.running = 0

    def reset_countdown(self):
        """ Reset the stopwatch. """
        self.start_time = time.time()
        self.elapsed_time = 0.0
        self.set_time(self.elapsed_time)

    def show_hint(self, msg):
        """ Show a hint"""
        # Check if exists for removal
        if self.hint_window:
            self.destroy_hint()
            
        self.hint_window = Toplevel(self.master)
        self.hint_window.geometry("1100x300+150+20")
        self.hint_window.overrideredirect(True)
        hint_text_label = Label(self.hint_window, bg='black', fg='white', font=("Arial", "20"), justify=LEFT, text="Indizio:")
        hint_text_label.pack(side=TOP, fill=BOTH)
        help_label = Label(self.hint_window, anchor=CENTER, justify=CENTER, fg="white", bg="black", font=("Arial", "30"), bd=4, relief=RAISED, text=msg)
        help_label.pack(side=BOTTOM, fill=BOTH, expand=1)
        hint_sound.play()

    def destroy_hint(self):
        self.hint_window.destroy()

    def show_video(self, file_name):
        proc = subprocess.Popen(['omxplayer', '-b', '-o', 'local', file_name])
        proc.wait()
        
    def activate_biohazard(self):
        self.biohazard_windo = Toplevel(self)
        self.biohazard_windo.geometry("1400x300+0+750")
        self.biohazard_windo.overrideredirect(True)
        self.frame = Frame(self.biohazard_windo, bg="black")
        #self.frame.grid()
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.columnconfigure(3, weight=1)
        self.frame.columnconfigure(4, weight=1)
        self.frame.columnconfigure(5, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        
        self.frame.pack(fill=BOTH, expand=1)
        self.label = Label(self.frame, bg="black", fg="red", font=("Arial", "30"), text="BOMBA BIOLOGICA ATTIVATA -- INSERIRE I CODICI PER DISATTIVARE")
        self.entry1 = Entry(self.frame, font=("Arial", "25"), width=12, bg="red")
        self.entry1.bind("<Return>", lambda event, entry_code=0: check_code(event, entry_code))
        
        self.entry2 = Entry(self.frame, font=("Arial", "25"), width=12, bg="red")
        self.entry2.bind("<Return>", lambda event, entry_code=1: check_code(event, entry_code))
        
        self.entry3 = Entry(self.frame, font=("Arial", "25"), width=12, bg="red")
        self.entry3.bind("<Return>", lambda event, entry_code=2: check_code(event, entry_code))
        
        self.entry4 = Entry(self.frame, font=("Arial", "25"), width=12, bg="red")
        self.entry4.bind("<Return>", lambda event, entry_code=3: check_code(event, entry_code))
        
        self.entry5 = Entry(self.frame, font=("Arial", "25"), width=12, bg="red")
        self.entry5.bind("<Return>", lambda event, entry_code=4: check_code(event, entry_code))
        
        self.entry6 = Entry(self.frame, font=("Arial", "25"), width=12, bg="red")
        self.entry6.bind("<Return>", lambda event, entry_code=5: check_code(event, entry_code))
        
        self.label.grid(row=0, column=0, columnspan=6)
        self.entry1.grid(row=1, column=0)
        self.entry2.grid(row=1, column=1)
        self.entry3.grid(row=1, column=2)
        self.entry4.grid(row=1, column=3)
        self.entry5.grid(row=1, column=4)
        self.entry6.grid(row=1, column=5)
        
        self.biohazard_windo.focus_set()
        
        """
        self.entry1.place(x=50, y=20, relwidth=0.15, relheight=0.3)
        self.entry2.place(x=240, y=20, relwidth=0.15, relheight=0.3)
        self.entry3.place(x=410, y=20, relwidth=0.15, relheight=0.3)
        self.entry4.place(x=630, y=20, relwidth=0.15, relheight=0.3)
        self.entry5.place(x=870, y=20, relwidth=0.15, relheight=0.3)
        self.entry6.place(x=1180, y=20, relwidth=0.15, relheight=0.3)
        """
    
    def game_over(self):
        self.game_over_window = Toplevel(self.master)
        self.game_over_window.geometry("1400x1050")
        #self.game_over_window.overrideredirect(True)
        self.game_over_window.wm_attributes('-fullscreen', True)
        self.game_over_label = Label(self.game_over_window, bg="black", fg="white", font=("DS-Digital", "200"), text="GAME OVER")
        self.game_over_label.pack(fill=BOTH, expand=1)
        alert = red_alert.play()
        self.after(10000, alert.stop)
        #alert.stop()
        self.after(11000, self.game_over_window.destroy)
        
    def processIncoming(self):
        # Handle all the messages currently in the queue (if any).
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                # Check contents of message and do what it says
                instruction = msg.rpartition('-')[0]
                instruction.strip()
                print(instruction)
                if instruction == "start_timer":
                    self.start_countdown()
                if instruction == "reset_timer":
                    self.stop_countdown()
                    self.reset_countdown()
                if instruction == "help":
                    hint_msg = msg.rpartition('-')[2]
                    print(hint_msg)
                    self.show_hint(hint_msg)
                if instruction == "destroy_help":
                    self.destroy_hint()
                if instruction == "video1":
                    self.show_video("./files/MisterX1.mp4")
                if instruction == "video2":
                    self.show_video("./files/MisterX2.mp4")
                if instruction == "biohazard":
                    self.activate_biohazard()

            except queue.Empty:
                pass


class ThreadedClient:
    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI. We spawn a new thread for the worker.
        """
        self.master = master

        # Create the queue
        self.queue = queue.Queue(1)

        # Set up the GUI part
        self.gui = GUI(master, self.queue)
        self.gui.pack(fill=BOTH, expand=1)

        #self.gui.activate_biohazard()

        # Setup socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(0)
        self.socket.bind((HOST, PORT))
        
        self.inputs = [self.socket]
        self.outputs = []

        # Set up the thread to do asynchronous I/O
        self.running = 1
        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()

    def periodicCall(self):
        """
        Check every # ms if there is something new in the queue.
        """
        self.gui.processIncoming()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.master.after(500, self.periodicCall)

    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select()'.
        One important thing to remember is that the thread has to yield
        control.
        """
        self.socket.listen()
        while self.running:
            read, write, exec = select.select(self.inputs, self.outputs, self.inputs)
            # Receiving the instructions names
            for s in read:
                if s is self.socket:
                    conn, addr = s.accept()
                    print("Connected by", addr)
                    conn.setblocking(0)
                    self.inputs.append(conn)
                else:
                    data = recv_timeout(s,2)
                    msg = b''.join(data).decode('utf-8')
                    self.queue.put(msg)

    def endApplication(self):
        self.running = 0
        self.socket.close()


rand = random.Random()
root = Tk()
root.geometry("1400x1050")
#root.overrideredirect(True)
root.wm_attributes('-fullscreen', True)
client = ThreadedClient(root)
root.protocol('WM_DELETE_WINDO', quit)
root.mainloop()