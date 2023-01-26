import cv2
from alright import WhatsApp
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk

from emojis_recognizer import EmojisRecognizer

EMOJIS_DIR = 'emoji_data/emoji'
emoji_index_to_path = {0: '1.png', 1: '2.png', 2: '3.png', 3: '4.png', 4: '5.png'}
emoji_index_to_sign = {0: '👆', 1: '✌', 2: '👌', 3: '🤘', 4: '🖖'}


def recognition(frame):
    """function for recognition of the hand emoji class form the frame"""
    # Creating emojis recognizer object
    emojis_recognizer = EmojisRecognizer(frame)
    # Finding the details of the hands in the frame
    hands_details = emojis_recognizer.find_hands_details()
    # Check if the frame contains hands
    if len(hands_details) == 0:
        return False, []
    # Converting the original image to hand images
    hand_images = emojis_recognizer.img2hands(hands_details)
    # Predicting the hand class of the hand images
    predictions = emojis_recognizer.predict_hand_class(hand_images, hands_details)
    # Converting the predictions to the corresponding emojis images
    emojis_recognizer.predictions2emojis(predictions)
    return True, predictions


def send(emoji_index, emoji_page):
    """function for sending the emoji to the desired contact"""
    emoji = EMOJIS_DIR + f'/{emoji_index_to_path[emoji_index]}'
    messenger.send_picture(emoji, 'emoji')
    text_success = Label(emoji_page)
    text_success.configure(text=f'successfully sent {emoji_index_to_sign[emoji_index]} ')
    text_success.pack()


def emojiWindow():
    """function for creating the page for emojis finding"""
    # Creating the page
    emoji_page = Tk()
    emoji_page.title('Hands Emojis')
    emoji_page.configure(bg='yellow')

    # Adding label to the page
    f1 = LabelFrame(emoji_page, height=50, width=50)
    f1.pack()
    l1 = Label(f1)
    l1.pack()

    emoji_index = 0

    # Adding button for sending the emoji
    send_button = Button(emoji_page, text="send", command=lambda: send(emoji_index, emoji_page))
    send_button.pack()

    # Opening of the camera
    cap = cv2.VideoCapture(0)

    while True:
        try:
            # Get image frame
            success, img = cap.read()
            if not success or img is None:
                continue

            # Finding the hand and predicting the class
            hand_exists, predictions = recognition(img)
            if len(predictions) > 0:
                emoji_index = predictions[0]

            # Displaying the frame on the screen
            img = ImageTk.PhotoImage(Image.fromarray(img))
            l1['image'] = img
            emoji_page.update()

        except Exception:
            print('ERROR')

    emoji_page.mainloop()


def findName():
    """function for finding the user name in whatsapp and opening the page for emojis sending"""
    messenger.find_by_username(entryName.get())
    opening.destroy()
    emojiWindow()


# The background structure
try:
    messenger = WhatsApp()
except:
    pass
input("Press ENTER after login into Whatsapp Web and your chats are visible.\n\n")

# Create object
opening = Tk()
opening.title('Hands Emojis')

# Add image file
image = Image.open("openingGUI.png")
resize_image = image.resize((400, 600))
img = ImageTk.PhotoImage(resize_image)

# Create Canvas
canvas1 = Canvas(opening, width=400, height=600)
canvas1.pack(fill="both", expand=True)

# Display image
canvas1.create_image(0, 0, image=img, anchor="nw")

# Create Buttons
entryName = Entry(opening, font=("arial", 20))
entryName_canvas = canvas1.create_window(202, 300, width=170, height=50, window=entryName)
searchButton = Button(opening, text="Search", command=findName)
searchButton_canvas = canvas1.create_window(127, 375, width=150, height=50, anchor="nw", window=searchButton)


while entryName.get() == 0:
    pass

# Execute tkinter
opening.mainloop()

