from tkinter import *
import random
import threading
import time


class TypeSpeedTest:

    def __init__(self):
        self.window = Tk()
        self.window.geometry("960x540")
        self.text_label = None
        self.entry = None
        self.all_words = []  # 200 random words from the words.csv
        self.strings = None  # 10 random words taken from all_words and displayed on the label
        self.user = []  # A list of the characters in the words that the user typed in
        self.given = []  # A list of the characters in the words that the user was given
        self.i = 0  # Counts every input into the text label
        self.word = 0  # Counts the words
        self.time_label = None
        self.run = True  # Flag for counter
        self.time = 20
        self.start_time = None
        self.remain = None  # Remaining time left
        self.cpm = 0  # The corrected characters per minute
        self.wpm = 0  # The corrected words per minute
        self.metric_label = None
        self.correct = 0  # Count of characters that were correct
        self.codes = ['Alt_L', 'Alt_R', 'Cancel', 'Caps_Lock', 'Control_L',
                      'Control_R', 'Delete', 'Down', 'End', 'Escape', 'Execute', 'F1', 'F2', 'Fi',
                      'F12', 'Home', 'Insert', 'Left', 'Linefeed', 'KP_0', 'KP_1', 'KP_2', 'KP_3',
                      'KP_4', 'KP_5', 'KP_6', 'KP_7', 'KP_8', 'KP_9', 'KP_Add', 'KP_Begin',
                      'KP_Decimal', 'KP_Delete', 'KP_Divide', 'KP_Down', 'KP_End', 'KP_Enter',
                      'KP_Home', 'KP_Insert', 'KP_Left', 'KP_Multiply', 'KP_Next', 'KP_Prior',
                      'KP_Right', 'KP_Subtract', 'KP_Up', 'Next', 'Num_Lock', 'Pause', 'Print',
                      'Prior', 'Return', 'Right', 'Scroll_Lock', 'Shift_L', 'Shift_R', 'Tab', 'Up']

    # Get list of words
    def get_words(self):
        with open('words.csv', 'r') as words:
            all_text = words.read().split(', ')
            word_list = [text for text in all_text]
            self.all_words = random.choices(word_list, k=200)

    # Show a timer
    def timer(self):
        self.start_time = 0
        frame = Frame(self.window)
        frame.pack()
        self.time_label = Label(frame, text=self.time)
        self.time_label.pack()

    # Create countdown function
    def countdown(self, e):
        if self.run:
            self.start_time = time.time()
            self.run = False
            while (time.time() - self.start_time) <= self.time:
                self.remain = round(self.time - (time.time() - self.start_time), 2)
                self.time_label.config(text=self.remain)
                self.time_label.update()
            else:
                self.entry.config(state='disable')
                final_chars = len(self.entry.get())
                # print(final_chars)
                if len(self.given) > 0:
                    self.given.append(" ")  # Adds a space to the given list if there are already characters in it
                    final_chars -= 1  # Reduces the length to append by 1 due to the space added
                else:
                    final_chars = final_chars
                for i in range(final_chars):
                    self.given.append(self.strings[i])
                [[self.user.append(char) for char in word] for word in self.entry.get()]
                # print(f"{self.strings}\n{self.given}\n{self.user}")
                # print(f"\n\n\n\n\n{self.given}\n{len(self.given)}\n{self.user}\n{len(self.user)}")
                for i in range(len(self.given)):
                    if self.given[i] == self.user[i]:
                        self.correct += 1
                self.cpm = int(self.correct * (60 / self.time))
                self.wpm = int(self.cpm / 5)
                text = f"Your CPM: {self.cpm}\n" \
                       f"Your WPM: {self.wpm}\n"
                self.metric_label.config(text=text)

    # Draw label for text corpus
    def text(self):
        frame = Frame(self.window, bg='black', height=150)
        frame.pack(pady=50, fill=BOTH, padx=10)
        self.strings = " ".join([str(item) for item in random.choices(self.all_words, k=10)])
        self.text_label = Label(frame, font='Arial', text=self.strings)
        self.text_label.pack(fill=BOTH)

    # Draw entry box for typing
    def show_entry(self):
        frame = Frame(self.window, bg='blue')
        frame.pack(fill=BOTH, pady=50, padx=10)
        self.entry = Entry(frame, font='Arial', justify='center')
        self.entry.pack(fill=BOTH)

    # Function to check the keys pressed
    def key_pressed(self, event):
        length = len(self.strings)
        # self.given =
        while self.i < length:
            if event.keysym == self.strings[self.i]:
                self.entry.config(fg='green')
                # print(self.strings[self.i], event.keysym, "right")
                self.i += 1
                break
            elif event.keysym == "BackSpace":
                if self.i < 0:
                    self.i = 0
                    break
                else:
                    self.i -= 1
                    break
            elif event.keysym in self.codes:
                break
            elif event.keysym == "space":
                self.entry.config(fg='green')
                self.i += 1
                # print(f"{self.strings.split()[self.word]}, {self.entry.get().split()[self.word]}")
                self.word += 1
                break
            else:
                self.entry.config(fg='red')
                # print(self.strings[self.i], event.keysym, 'wrong')
                self.i += 1
                break
        else:
            [[self.user.append(char) for char in word] for word in self.entry.get()]
            if len(self.given) > 0:
                self.given.append(" ")
            [[self.given.append(char) for char in word] for word in self.strings]
            # print(f"{self.user}\n{self.given}")
            # print(f"{self.strings}\n{self.given}\n{self.user}")
            self.word = 0
            self.strings = " ".join([str(item) for item in random.choices(self.all_words, k=10)])
            self.text_label.config(text=self.strings)
            self.entry.delete(0, END)
            self.i = 0

    def metric(self):
        frame = Frame(self.window)
        frame.pack()
        text = f"Your CPM: {self.cpm}\n" \
               f"Your WPM: {self.wpm}\n"
        self.metric_label = Label(frame, text=text)
        self.metric_label.pack()

    def draw(self):
        self.get_words()
        self.timer()
        self.text()
        self.show_entry()
        self.metric()
        self.entry.bind("<Key>", self.key_pressed)
        threading.Thread(target=self.window.bind, args=('<Key>', self.countdown)).start()
        self.window.mainloop()


speed_test = TypeSpeedTest()
speed_test.draw()
