from tkinter import *
import simpleaudio as sa
from time import sleep

codes = ["ABCDE", "ABCDE", "ABCDE", "ABCDE", "ABCDE"]

deactivation_audio = sa.WaveObject.from_wave_file("./finalver/shut_down.wav")
wrong_audio = sa.WaveObject.from_wave_file("./finalver/red_alert.wav")

count = 0


def reset(event, window):
    global count
    count = 0
    event.widget.focus_set()
    window.__init__(event.widget)


def check_code(event, entry_code, canvas, status_text):
    global count
    text = event.widget.get()
    if text == codes[entry_code]:
        canvas.itemconfig(status_text, fill="green", text="DISABLED", font=("Monospace", "12"))
        event.widget.config(state=DISABLED)
        event.widget.unbind("<Return>")
        deactivation_audio.play()
        count = count + 1
        event.widget.master.master.focus_set()
    else:
        event.widget.delete(0, END)
        wrong = wrong_audio.play()
        sleep(2.9)
        wrong.stop()
        event.widget.master.master.focus_set()

    #final_splash_screen
    if count == 5:
        elements = canvas.find_all()
        entries = event.widget.master.place_slaves()

        for en in entries:
            en.place_forget()

        for el in elements:
            canvas.delete(el)

        canvas.config(bg="black")
        canvas.create_text(640, 100, text="MISSIONE COMPIUTA", font=("Monospace", "50"), fill="green")
        canvas.create_text(640, 370, text="HAI DISINNESCATO TUTTE LE\rTESTATE NUCLEARI."
                                          "\rESCI IN FRETTA DAL BUNKER\rE' RIMASTO POCO TEMPO!",
                           font=("Monospace", "40"), fill="white", justify=CENTER)
        event.widget.master.master.focus_set()


class Application(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=1)
        self.create_screen()

    def create_screen(self):
        #background
        self.background_image = PhotoImage(file="./finalver/MissileImage.png")
        self.background = Canvas(self, width=1280, height=720, highlightthickness=0)
        self.background.create_image(640, 360, image=self.background_image)
        self.background.bind("<Return>", reset)
        self.background.pack(fill="both", expand=1)

        #city texts
        self.background.create_text(122, 560, text="WASHINGTON", font=("Monospace", "23"), fill="white")
        self.background.create_text(382, 560, text="LONDRA", font=("Monospace", "23"), fill="white")
        self.background.create_text(642, 560, text="MOSCA", font=("Monospace", "23"), fill="white")
        self.background.create_text(898, 560, text="PECHINO", font=("Monospace", "23"), fill="white")
        self.background.create_text(1162, 560, text="TOKYO", font=("Monospace", "23"), fill="white")

        #status texts
        self.background.create_text(75, 590, text="Status:", font=("Monospace", "15"), fill="white")
        a0 = self.background.create_text(165, 590, text="ACTIVE", font=("Monospace", "15"), fill="red")

        self.background.create_text(340, 590, text="Status:", font=("Monospace", "15"), fill="white")
        a1 = self.background.create_text(430, 590, text="ACTIVE", font=("Monospace", "15"), fill="red")

        self.background.create_text(600, 590, text="Status:", font=("Monospace", "15"), fill="white")
        a2 = self.background.create_text(690, 590, text="ACTIVE", font=("Monospace", "15"), fill="red")

        self.background.create_text(850, 590, text="Status:", font=("Monospace", "15"), fill="white")
        a3 = self.background.create_text(940, 590, text="ACTIVE", font=("Monospace", "15"), fill="red")

        self.background.create_text(1110, 590, text="Status:", font=("Monospace", "15"), fill="white")
        a4 = self.background.create_text(1200, 590, text="ACTIVE", font=("Monospace", "15"), fill="red")


        #Entry boxes
        self.entry0 = Entry(self, font=("Monospace", "23"), width=9, justify=CENTER, bd=4, bg="red")
        self.entry0.place(x=20, y=615, relwidth=0.16, relheight=0.1)

        self.entry0.bind("<Return>", lambda event, entry_code=0, canvas=self.background,
                                            status_text=a0: check_code(event, entry_code, canvas, status_text))

        self.entry1 = Entry(self, font=("Monospace", "23"), width=9, justify=CENTER, bd=4, bg="red")
        self.entry1.place(x=285, y=615, relwidth=0.16, relheight=0.1)

        self.entry1.bind("<Return>", lambda event, entry_code=1, canvas=self.background,
                                            status_text=a1: check_code(event, entry_code, canvas, status_text))

        self.entry2 = Entry(self, font=("Monospace", "23"), width=9, justify=CENTER, bd=4, bg="red")
        self.entry2.place(x=545, y=615, relwidth=0.16, relheight=0.1)

        self.entry2.bind("<Return>", lambda event, entry_code=2, canvas=self.background,
                                            status_text=a2: check_code(event, entry_code, canvas, status_text))

        self.entry3 = Entry(self, font=("Monospace", "23"), width=9, justify=CENTER, bd=4, bg="red")
        self.entry3.place(x=800, y=615, relwidth=0.16, relheight=0.1)

        self.entry3.bind("<Return>", lambda event, entry_code=3, canvas=self.background,
                                            status_text=a3: check_code(event, entry_code, canvas, status_text))

        self.entry4 = Entry(self, font=("Monospace", "23"), width=9, justify=CENTER, bd=4, bg="red")
        self.entry4.place(x=1060, y=615, relwidth=0.16, relheight=0.1)

        self.entry4.bind("<Return>", lambda event, entry_code=4, canvas=self.background,
                                            status_text=a4: check_code(event, entry_code, canvas, status_text))


root = Tk()
root.geometry("1280x720")
#root.overrideredirect(True)
#root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
app = Application(root)
root.bind("<F10>", lambda event, window=app: reset(event, window))
root.mainloop()
