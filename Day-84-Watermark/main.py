import os
import time
from tkinter import *
from tkinter import filedialog as fd
from PIL import ImageTk, Image, ImageFont, ImageDraw2


class WaterMarker:

    def __init__(self):
        self.window = None
        self.img_frame = None
        self.img = None
        self.add_image = None
        self.button_frame = None
        self.text_entry = None
        self.mark_image = None
        self.name = None
        self.label = None
        self.open_image = None

    # This opens an ask open file dialog from the tkinter module in order to pick the image that you want to watermark
    def adds_image(self):
        filetypes = (('image files', ('*.jpg', '*.png*', '*.png', '*.svg', '*.webp')),
                     ('All files', '*.*'))
        filenames = fd.askopenfilenames(title='Pick Images',
                                        initialdir='/',
                                        filetypes=filetypes)
        for filename in filenames:
            self.label.update()
            height = self.label.winfo_height()
            width = self.label.winfo_width()
            image = Image.open(filename)
            resized_image = image.resize((width, height), Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(resized_image)
            picture = Image.open(filename)
            self.name = filename.split('/')[-1]
            picture.save(f'image/{self.name}')
            self.label.configure(image=self.img)

    # This adds a watermark on the image, I could not show the watermarked image dynamically
    def marks_image(self):
        image = Image.open(f'image/{self.name}')
        width, height = image.size
        font_ = ImageFont.truetype("arial.ttf", 46)
        text = self.text_entry.get()
        edit_image = ImageDraw2.Draw(image)
        edit_image.text((width / 1.5, height / 1.5), text=text, font=font_, color="red")
        self.text_entry.insert(0, "Creating Your WaterMark...")
        image = image.convert('RGB')
        image.save(f"watermarked/watermarked-{self.name}")
        time.sleep(1.5)
        self.img = ImageTk.PhotoImage(file=f'watermarked/watermarked-{self.name}')
        self.label.configure(image=self.img)
        self.open_image.config(state='normal')
        self.text_entry.delete(0, END)

    # When the show watermarked button is clicked, file explorer opens the location in which it was saved
    def shows_image(self):
        directory = 'watermarked'
        parent_dir_ = os.path.join(os.getcwd(), directory)
        file_ = os.path.join(parent_dir_, f"watermarked-{self.name}")
        if os.path.isfile(file_):
            os.startfile(parent_dir)

    # This dynamically resizes the image when the window is resized
    def img_resizer(self, e):
        try:
            bg1 = Image.open(f"image/{self.name}")
        except AttributeError:
            pass
        except FileNotFoundError:
            pass
        else:
            resized_bg = bg1.resize((e.width, e.height - 5), Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(resized_bg)
            self.label.configure(image=self.img)

    def image_frame(self, window):
        self.img_frame = Frame(window, bg='white')
        self.img_frame.pack(side=TOP, fill=BOTH, expand=True)
        self.label = Label(self.img_frame, image=self.img, bg='gray')
        self.label.pack(fill=BOTH, expand=True)

    def add_buttons_frame(self, window):
        self.button_frame = Frame(window, width=400, height=1, bg='white')
        self.button_frame.pack(side=BOTTOM, fill=X)

    def add_button(self, button_frame):
        self.add_image = Button(button_frame, text='Add Images', command=self.adds_image)
        self.add_image.pack(fill=BOTH, padx=10, pady=10, side=LEFT)

    def show_button(self, button_frame):
        self.open_image = Button(button_frame, text='Open Watermarked image',
                                 command=self.shows_image, state='disabled')
        self.open_image.pack(side=LEFT, fill=BOTH, padx=10, pady=10)

    def mark_button(self, button_frame):
        self.mark_image = Button(button_frame, text='Mark Image', command=self.marks_image)
        self.mark_image.pack(fill=BOTH, padx=10, pady=10, side=RIGHT)

    def get_text(self, button_frame):
        width = 500
        height = 20
        text_canvas = Canvas(button_frame, bg='black', width=width, height=height)
        text_canvas.pack(side=RIGHT, padx=10, pady=10)
        self.text_entry = Entry(text_canvas)
        self.text_entry.pack(fill=BOTH, expand=True)
        text_canvas.create_window(width / 2, height / 2, window=self.text_entry, anchor='center',
                                  height=height, width=width)

    def draw(self):
        # Draw window
        self.window = Tk()
        self.window.title('Water Marker')
        self.window.iconbitmap('icon.png')
        self.window.geometry("960x540")
        self.window.minsize(width=960, height=540)
        self.window.maxsize(width=1920, height=1080)
        # Frame for image
        self.image_frame(self.window)
        # Create frame for buttons
        self.add_buttons_frame(self.window)
        # Button to select image
        self.add_button(self.button_frame)
        # Button to show image in path
        self.show_button(self.button_frame)
        # Button to make mark on image
        self.mark_button(self.button_frame)
        # Entry to get the watermark text
        self.get_text(self.button_frame)
        self.label.update()
        self.label.bind('<Configure>', self.img_resizer)
        self.window.mainloop()


# self.button_frame =

# Makes directory to save images if directory is not already there
directories = ['image', 'watermarked']
parent_dir = os.getcwd()
for dire in directories:
    if os.path.isdir(os.path.join(parent_dir, dire)):
        pass
    else:
        path = os.path.join(parent_dir, dire)
        os.mkdir(path)

# Initializes the class
water_marker = WaterMarker()
water_marker.draw()

# Clears the folder that contains the image without the watermark
folder = os.getcwd().replace('\\', '/')
for file in os.listdir(f"{folder}/image"):
    if file:
        file = file.replace('\\', '/')
        file_path = f"{folder}/image/{file}"
        os.remove(file_path)
