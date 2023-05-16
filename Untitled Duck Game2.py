from tkinter import HIDDEN, NORMAL, Tk, Canvas
import pygame

#starts tkinter and opens a window
root = Tk()
root.title('Untitled Duck Game')

c = Canvas(root, width=400, height=400)
c.configure(bg='teal', highlightthickness=0)
#Other good background options are turquoise and plum, but they're kind of Easter-ish

#initialise the pygame mixer in order to play the audio file
pygame.mixer.init()

#calls the audio file, is used during the 'tickle' function
def play():
    pygame.mixer.music.load("single-duck-quack-sound-effect.mp3")
    pygame.mixer.music.play(loops=0)

#body color
c.body_color = 'cornsilk'
#feet
c.accent_color = 'darkorange'
#outline and mouth color
c.outline_color = 'gold'

#define individual foot movements
def step_left():
    c.move(foot_left, 0, 5)
    c.move(foot_right, 0, -5)

def step_right():
    c.move(foot_left, 0, -5)
    c.move(foot_right, 0, 5)

#define toggling from foot to foot
def toggle_feet():
     if not c.step_left:
          step_left()
          step_right()
          step_left()
          c.step_left = True
     else:
          step_right()
          step_left()
          step_right()
          c.step_left = False

#start the toggled movement
def walk():
     toggle_feet()
     root.after(5000, toggle_feet)
     root.after(2000, walk)     

#define arm movement
def toggle_arms():
    if not c.arms_up:
          c.move(arm_left, -10, -10)
          c.move(arm_right, 10, -10)
          c.arms_up = True
    else:
         c.move(arm_left, 10, 10)
         c.move(arm_right, -10, 10)
         c.arms_up = False

#start arm movment
def flap():
     toggle_arms()
     toggle_arms()
     toggle_arms()
     root.after(500, toggle_arms)
     root.after(5000, flap)

#define toggling from open eyes to closed eyes
def toggle_eyes():
    current_state = c.itemcget(pupil_left, 'state')
    new_state = NORMAL if current_state == HIDDEN else HIDDEN
    c.itemconfigure(pupil_left, state=new_state)
    c.itemconfigure(pupil_right, state=new_state)

#start the process of blinking
def blink():
    toggle_eyes()
    root.after(250,toggle_eyes)
    root.after(3000, blink)

#defines pupil movement for the 'tickle' event
def toggle_pupils():
    if not c.eyes_crossed:
          c.move(pupil_left, 10, -5)
          c.move(pupil_right, -10,-5)
          c.itemconfigure(pupil_left_blink, state=HIDDEN)
          c.itemconfigure(pupil_right_blink, state=HIDDEN)
          c.eyes_crossed = True
    else:
         c.move(pupil_left, -10, 5)
         c.move(pupil_right, 10, 5)
         c.itemconfigure(pupil_left_blink, state=NORMAL)
         c.itemconfigure(pupil_right_blink, state=NORMAL)
         c.eyes_crossed = False

def tickle(event):
     play()
     toggle_mouth()
     toggle_pupils()
     hide_happy(event)
     root.after(1000, toggle_mouth)
     root.after(1000, toggle_pupils)
     return

#toggles mouth movement for tickle event
def toggle_mouth():
    if not c.mouth_out:
          c.itemconfigure(mouth_react, state=NORMAL)
          c.itemconfigure(snout__top_react, state=NORMAL)
          c.itemconfigure(snout__bottom_react, state=NORMAL)
          c.itemconfigure(snout_top, state=HIDDEN)
          c.itemconfigure(snout_bottom, state=HIDDEN)
          c.itemconfigure(cheek_left_react, state=NORMAL)
          c.itemconfigure(cheek_right_react, state=NORMAL)
          c.itemconfigure(cheek_left, state=HIDDEN)
          c.itemconfigure(cheek_right, state=HIDDEN)
          c.mouth_out = True
    else:
        c.itemconfigure(mouth_react, state=HIDDEN)
        c.itemconfigure(snout__top_react, state=HIDDEN)
        c.itemconfigure(snout__bottom_react, state=HIDDEN)
        c.itemconfigure(snout_top, state=NORMAL)
        c.itemconfigure(snout_bottom, state=NORMAL)
        c.itemconfigure(cheek_left_react, state=HIDDEN)
        c.itemconfigure(cheek_right_react, state=HIDDEN)
        c.itemconfigure(cheek_left, state=NORMAL)
        c.itemconfigure(cheek_right, state=NORMAL)
        c.mouth_out = False

#Reaacts when you mouse over the duck 
#turns the cheeks a different color and bringing the happiness level back up to max amount
def show_happy(event):
    if (87 <= event.x <= 313) and (25 <= event.y <= 375):
        c.itemconfigure(cheek_left_happy, state=NORMAL)
        c.itemconfigure(cheek_right_happy, state=NORMAL)
        c.itemconfigure(cheek_left, state=HIDDEN)
        c.itemconfigure(cheek_right, state=HIDDEN)
        c.happy_level = 10
        # level 10 is about a minute, 200 would be 20 min
    return

#hides the 'happy' reaction to allow the 'tickle' reaction
def hide_happy(event):
        c.itemconfigure(cheek_left_happy, state=HIDDEN)
        c.itemconfigure(cheek_right_happy, state=HIDDEN)
        c.itemconfigure(cheek_left, state=NORMAL)
        c.itemconfigure(cheek_right, state=NORMAL)
        return

#when happiness gets to 0 the duck gets grumpy until you trigger the 'happy' reaction
def mad():
    if c.happy_level == 0:
          c.itemconfigure(eyebrow_left, state=NORMAL)
          c.itemconfigure(eyebrow_right, state=NORMAL)
          c.configure(bg='maroon', highlightthickness=0)
    else:
          c.itemconfigure(eyebrow_left, state=HIDDEN)
          c.itemconfigure(eyebrow_right, state=HIDDEN)
          c.configure(bg='teal', highlightthickness=0)
          c.happy_level -= 1
    root.after(5000, mad)
          

#draw the body parts   
foot_left = c.create_oval(100, 340, 190, 390, outline=c.outline_color, fill=c.accent_color)
foot_right = c.create_oval(210, 340, 300, 390, outline=c.outline_color, fill=c.accent_color)

body = c.create_oval(80, 150, 320, 375, outline=c.outline_color, fill=c.body_color)
body = c.create_oval(87, 25, 313, 245, outline=c.outline_color, fill=c.body_color)

arm_left = c.create_oval(15, 180, 120, 230, outline=c.outline_color, fill=c.body_color)
arm_right = c.create_oval(280, 180, 385, 230, outline=c.outline_color, fill=c.body_color)

#covers part of the wing ovals for a better look
tummy = c.create_oval(100, 150, 300, 250, outline=c.body_color, fill=c.body_color)

#inside of the mouth that only shows when the 'tickle' function is called
mouth_react = c.create_oval(170, 80, 230, 170, outline=c.body_color, fill='lightcoral', state=HIDDEN)

snout_top = c.create_oval(150, 100, 250, 130, outline=c.outline_color, fill=c.outline_color)
snout_bottom = c.create_oval(150, 124, 250, 154, outline=c.outline_color, fill=c.outline_color)

#open snout/bill that gets toggled during the 'tickle' function
snout__top_react = c.create_oval(150, 80, 250, 120, outline=c.outline_color, fill=c.outline_color, state=HIDDEN)
snout__bottom_react = c.create_oval(150, 144, 250, 174, outline=c.outline_color, fill=c.outline_color, state=HIDDEN)


cheek_left = c.create_oval(110, 110, 145, 145, outline=c.body_color, fill='antiquewhite')
cheek_right = c.create_oval(255, 110, 290, 145, outline=c.body_color, fill='antiquewhite')

#gets called during 'show happy'
cheek_left_happy = c.create_oval(110, 110, 145, 145, outline='pink', fill='pink', state=HIDDEN)
cheek_right_happy = c.create_oval(255, 110, 290, 145, outline='pink', fill='pink', state=HIDDEN)

#gets called during 'tickle'
cheek_left_react = c.create_oval(110, 110, 145, 145, outline='lightcoral', fill='lightcoral', state=HIDDEN)
cheek_right_react = c.create_oval(255, 110, 290, 145, outline='lightcoral', fill='lightcoral', state=HIDDEN)

#gets called during 'mad'
eyebrow_left = c.create_line(129, 70, 153, 80, smooth=1, width=2, state=HIDDEN)
eyebrow_right = c.create_line(246, 80, 270, 70, smooth=1, width=2, state=HIDDEN)

#closed eyes
pupil_left_blink = c.create_oval(134, 85, 151, 90, outline='black', fill='black')
pupil_right_blink = c.create_oval(249, 85, 266, 90, outline='black', fill='black')

#open eyes
pupil_left = c.create_oval(133, 79, 151, 96, outline='black', fill='black')
pupil_right = c.create_oval(248, 79, 266, 96, outline='black', fill='black')

#renders everything in the window
c.pack()


#input events 
c.bind('<Motion>', show_happy)
c.bind('<Leave>', hide_happy)
#double-1 is tkinter's double-click
c.bind('<Double-1>', tickle)

#define stating info
#happiness lvl 10 lasts about a minute
#change it to 200 here and in show_happy() to get 20 min before  mad()
c.happy_level = 10
c.eyes_crossed = False
c.mouth_out = False
c.step_left = False
c.arms_up = True


#starting the root functions for behaviors
root.after(1000, blink)

root.after(5000, mad)

root.after(3000, walk)

root.after(3000, flap)

#starts the function that looks out for input events ie. mouse clicks
root.mainloop()

