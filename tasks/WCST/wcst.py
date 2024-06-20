#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division
import pandas as pd
import os

from psychopy import visual, core, event, sound, prefs, gui, data, logging
import random
from psychopy.hardware import keyboard
import yaml
from datetime import datetime

date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# Path to the YAML file contains the language and experiment configurations
config_path = f'configs/config.yaml'
experiment_config_path = f'configs/experiment.yaml'

# Load the YAML file
with open(config_path, 'r', encoding="utf-8") as file:
    config_data = yaml.safe_load(file)
language = config_data['language']
country_code = config_data['country_code']
lab_number = config_data['lab_number']
random_seed = config_data['random_seed']
font = config_data['font']

if os.path.exists(experiment_config_path):
    # Load the experiment configuration if the file exists
    with open(experiment_config_path, 'r', encoding="utf-8") as file:
        expInfo = yaml.safe_load(file)
        participant_id_str = str(expInfo['participant_id'])
        while len(participant_id_str) < 3:
            participant_id_str = "0" + participant_id_str
        participant_id = participant_id_str
else:
    # Set default values if the file does not exist
    expInfo = {'participant_id': 999, 'session_id': 2}

# Store info about the experiment session
psychopyVersion = '2023.2.3'
expName = 'WCST'  # from the Builder filename that created this script


# Create folder name for the results
results_folder = f"{participant_id}_{language}_{country_code}_{lab_number}_PT{expInfo['session_id']}"

# Create folder for audio and csv data
output_path = f'data/psychometric_test_{language}_{country_code}_{lab_number}/WCST/{results_folder}/'
os.makedirs(output_path, exist_ok=True)

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = f"{output_path}" \
           f"{language}{country_code}{lab_number}" \
           f"_{participant_id}_PT{expInfo['session_id']}_{date}"
game_data = []

instructions_df = pd.read_excel(f'languages/{language}/instructions/WCST_instructions_{language.lower()}.xlsx', index_col='screen')
welcome_text = instructions_df.loc['Welcome_text', language]
welcome_text = welcome_text.replace('\\n', '\n')
success_text = instructions_df.loc['success_text', language]
success_text = success_text.replace('\\n', '\n')
fail_text = instructions_df.loc['fail_text', language]
fail_text = fail_text.replace('\\n', '\n')
instructions = instructions_df.loc['WCST_instructions', language]
instructions = instructions.replace('\\n', '\n')
summary_text = instructions_df.loc['summary_text', language]
summary_text = summary_text.replace('\\n', '\n')
summary_text_list = summary_text.split('\n')
Goodbyetext = instructions_df.loc['Goodbye_text', language]
Goodbyetext = Goodbyetext.replace('\\n', '\n')

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame


# CLASSES
class Card:
    """
    A card class that creates playing card objects.
    Attributes:
    -----------
    number : int
        The number associated with the card
    shape : str
        The shape of the card (e.g., "circle", "square").
    color : str
        The color of the card

    Methods:
    --------
    get_card_property(prop) -> str:
        Returns the requested property of the card. `prop` can be "number", "shape", or "color".

    get_filename() -> str:
        Returns the filename of the image associated with the card.
        _CAUTION_
        Sett window before initialzing any cards.
        Dependent on correct image_path: Sett inside the class. 
        As of now, only works if you actually have png files at the image_path, that are named following the format: number_shape_color.png
        
    get_psychopy(position) -> obj
        Creates a PsychoPy ImageStim object representing the card.
    """
    
    #The directory path where card images are stored and card_size.
    image_path = "./tasks/WCST/cards/"
    card_size = (128,176)
    _pos = None
    window = None
    
    @classmethod
    def set_window(cls,window):
        cls.window = window
    
    def __init__(self,number,shape,color):
        self.number = number
        self.shape = shape
        self.color = color
        self.psypy = self.create_psychopy()
     
        
    def get_card_property(self, prop):
        """
        Function returns one of the properties of the card.
        prop is one of "number", "shape" or "color"
        """
        if prop=="number":
            return self.number
        elif prop=="shape":
            return self.shape
        elif prop=="color":
            return self.color
        else:
            raise AttributeError("Unknown atttribute")
    
    def __repr__(self):
        """
        Returns the string representation of the card object
        str: Card(number,shape,color)
        """
        return "{num},{shape},{color}".format(num=self.number,shape=self.shape, color=self.color)
    
    def get_filename(self): # property possibility
        """Return filename of the image file for that card"""
        fname = os.path.join(self.image_path, "%i_%s_%s.png"%(self.number, self.shape, self.color))
        return fname
    
    def create_psychopy(self, position=(0,0), **kwargs):
        """
        Creates a PsychoPy ImageStim object representing the card.
    
        Parameters:
        -----------
        position : tuple of int, optional
            The (x, y) coordinates for the position of the image in the window.
            Defaults to (0, 0).
    
        Returns:
        --------
        A PsychoPy ImageStim object with the card's image set at the specified position.
        """
        if not Card.window:
            raise ValueError("The window attribute for Card is not set. Use Card.set_window() and give the class a valid psychopy window configuration.")
        ppy_repr = visual.ImageStim(Card.window,image=self.get_filename(),size=(self.card_size),pos=(position), **kwargs)
        return ppy_repr
        
    @property
    def pos(self):
        return self._pos
    
    @pos.setter
    def pos(self, value):
        self._pos = value
        self.psypy.pos = value

        
    def render(self):
        self.psypy.draw()
        
    @property
    def rect(self):
        """A method that gives the cordinates of the card: Used when looking for mouse clicks"""
        width, height = self.card_size
        xpos, ypos = self.psypy.pos
        left = xpos - width / 2
        right = xpos + width / 2
        top = ypos + height / 2
        bottom = ypos - height / 2

        return [left, top, right, bottom]
        

class Stack():
    
    """
    A class that simulates a stack, akin to a deck of cards.
    
    Attributes:
    -----------
    list_of_cards : list[Card1,Card2,Card3]
        A list containing objects of the Card class.
        
    Methods:
    --------
    add(new_card: Card) -> None:
        Adds the given card to the top of the stack.
    
    pop() -> Card:
        Removes and returns the card from the top of the stack.
    
        _CAUTION_
        THe end of the list is conceptualized as the top of the stack
    
    render()
        A function that takes the card at the top of the stack and renders it on screen as psychopy image.
        Also, updates the card with a position argument corresponding to its stack.
    """

    
    def __init__(self,list_of_cards):
        self.list_of_cards = list_of_cards
        
    def __repr__(self):
        return repr(self.list_of_cards)
    
    def __len__(self):
        return len(self.list_of_cards)
    
    def add(self,new_card):
        self.list_of_cards.append(new_card)
    
    def pop(self):
        return self.list_of_cards.pop()
    
    def render(self):
        if self.list_of_cards:
            card = self.list_of_cards[-1]
            card.pos = (self.xpos, self.ypos)
            card.render()


class MainStack(Stack):
    """
    This is the player deck. Its a subclass of the stack class.
    Compiles a a list of card objects and gives it a cordinate position.
    
    Contains data:
        Contains lists of card attributes.
        -numbers-list[int]
        -shapes -list[str]
        -colors -list[str]
        -xpos   -int
        -ypos   -int
    """
    
    xpos = 0
    ypos = -350
    numbers = [1,2,3,4]
    shapes = ["circle","square","triangle","star"]
    colors = ["blue","green","red","yellow"]
    
    def __init__(self):
        self.list_of_cards = []
        for i in self.numbers:
            for y in self.shapes:
                for x in self.colors:
                    card = Card(i,y,x)
                    self.list_of_cards.append(card)
        random.shuffle(self.list_of_cards)
        
    

class DiscardStack(Stack):
    """
    This is a multistack. Its a subclass of the stack class.
    A representation of the stimulus cards and their corresponding discard piles.
    Compiles the stimulus decks and gives them the presett card, rendering cordinates and a clickbox.
    Contains data:
        -xpos_stimcard   -int
        -ypos_discard   -int
        -stimdesign    -dict : contains text information for psychoppy textStim object : Can be changed in class for visual customization.
    Method
    ------
    render()
    Contains a custom renderingg method, specific for this multistack.
    It will always draw the stimulus card, and if there are cards present in the discard stack, the top card will be rendered.
    Additionally, it will draw a psychopy text object on top of the stimulus card, indicating keybord input for choosing that stimulus card.
    """
    
    ypos_stimcard = 300
    ypos_discard = 110
    
    stimdesign  = {
    'font': font,
    'height': 42,
    'color': 'white',
    'bold': True
    }
    
    def __init__(self, num):
        self.list_of_cards=[]
        self.stimulus_card=None
        if num==1:
            self.xpos = -300
            self.stimulus_card=Card(1, "triangle", "red")

        elif num==2:
            self.xpos = -100
            self.stimulus_card=Card(2, "star", "green")
           
        elif num==3:
            self.xpos =  100
            self.stimulus_card=Card(3, "square", "yellow")
          
        elif num==4:
            self.xpos =  300
            self.stimulus_card=Card(4, "circle", "blue")
            
        self.stimulus_card.pos = (self.xpos, self.ypos_stimcard)
        
    def __repr__(self):
        if len(self.list_of_cards)>0:
            card=self.list_of_cards[-1]
        else:
            card="<empty>"
        return "DiscardStack(%s, %s)"%(self.stimulus_card, card)
        
    def render(self):
        # render the stimulus card
        self.stimulus_card.pos = (self.xpos, self.ypos_stimcard)
        self.stimulus_card.render()
        # if there are cards in the discard stack render the top card
        if self.list_of_cards:
            card=self.list_of_cards[-1]
            card.pos = (self.xpos, self.ypos_discard)
            card.render()
        # render the number on top of the stack
        add = {
        'text': self.stimulus_card.number,
        'pos': (self.xpos, self.ypos_stimcard + 110)
        }
        design = DiscardStack.stimdesign.copy()
        design.update(add)
        stim_text = visual.TextStim(win, **design)
        stim_text.draw()




    
# FUNCTIONS

def track(data_point, trial):
    trial.append(data_point)
    return trial

def matched_category(rules,choice,card,stim_card):
    """" parameters: 
        a function that takes in, a list of matching categories 'aka' rules, and two card objects
        returns: a list of strings that contain the categories on which the cards are matched """
    matched = []
    for rule in rules:
        if card.get_card_property(rule) == stim_card.get_card_property(rule):
            matched.append(rule)
    return matched
    

def random_key(key_length):
    """A function that makes a random string of letters and numbers
    Parameters: lenght of string as int
    Returns: -> str
    """
    key = []
    alpha = "abcdefghijklmnopqrstuvwxyz"
    num = "123456789"
    for i in range(key_length):
        l = random.choice(alpha)
        n = random.choice(num)
        if int(n) % 2 == 0:
            l = l.capitalize()
        key.append(l + n)
    return ''.join(key)

    
    
def save_results(data, filename):
    index = ["rt", "card", "chosen card", "success", "matched on categories", "active rule", "win streak"]
    game_data_dicts = []

    for trial_data in data:
        trial_dict = {}
        for i, field in enumerate(index):
            trial_dict[field] = trial_data[i]
        game_data_dicts.append(trial_dict)

    df = pd.DataFrame(game_data_dicts)
    output_filename = f"{filename}.csv"
    df.to_csv(output_filename, index=False)

    

def results(data):
    holder = "blank"
    preservative_error = 0
    index = ["rt", "card","chosen card", "success", "matched on categories", "active rule",  "win streak"]
    # procent_correct
    win_list = [item[3] for item in data]
    total_correct = sum(win_list)
    total_number = len(win_list)
    procent_correct = total_correct /total_number * 100
    
    # Categories completed
    win_streak = [item[6]for item in data]
    completed = [item[6] for item in data if item[6] == 5]
    completed_categories = len(completed)
    
    # Error type
    active_rule = [item[5] for item in data]
    matched_categories = [item[4] for item in data]
    
    for index, (win, rule, matched, streak) in enumerate(zip(win_list, active_rule, matched_categories, win_streak)):
        print(index)
        if streak == 5:
            holder = rule
        if win == False and holder in matched:
            preservative_error += 1
    
    return procent_correct, completed_categories, preservative_error
    
# TEXTS

intro = {
    'text': welcome_text,
    'font': font,
    'height': 36,
    'wrapWidth': 1000,
    'color': 'black',
    'bold': False,
    'italic': False,
    'pos': (0, 0)
}

instruct = {
    'text': instructions,
    'font': font,
    'height': 30,
    'wrapWidth': 1000,
    'color': 'black',
    'bold': False,
    'italic': False,
    'pos': (0, 0)
}

success = {
    'text': success_text,
    'font': font,
    'height': 42,
    'color': 'green',
    'bold': True,
    'italic': False,
    'pos': (0, -100)
}

fail = {
    'text': fail_text,
    'font': font,
    'height': 42,
    'color': 'red',
    'bold': True,
    'italic': False,
    'pos': (0, -50)
}


# GAME_SETUP

# Window settings
win = visual.Window(
    size=[1440, 900], fullscr=True, screen=0,
    # winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, units="pix")

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()

Card.set_window(win) # Pass in the window for the card class


# Create stacks of cards
mainstack = MainStack()
dstacks = {i:DiscardStack(i) for i in range(1,5)}

# initialize
rules = ["shape", "color", "number"]
active_rule = random.choice(rules)
win_streak=0
# text_input = visual.TextBox2(win=window, text='Write your username: ')

#SOUNDS
 #Create a sound object from an audio file
sound_file = "./tasks/WCST/sounds/win.wav"
win_music = sound.Sound(sound_file)
sound.init()

#LOGO
# logo = visual.ImageStim(window,image="../logo/logo.png",pos=(0,300),size=(300,300))

# GAME


# Start screen
intro_txt = visual.TextStim(win, **intro)
start_key = "space"
end_key = "escape"
keys_clock = core.Clock()

while True:
    # logo.draw()
    intro_txt.draw()
    win.flip()
    keys_clock.reset()

    # Check for keypresses
    keys = event.getKeys(keyList=[start_key, end_key], timeStamped=keys_clock)

    for key, rt in keys:
        if key == start_key:
            break
        elif key == end_key:
            win.close()
            core.quit()
    else:
        continue
    break

    
## instructions
instruction = visual.TextStim(win, **instruct)
while True:
    
    instruction.draw()
    win.flip()
    keys_clock.reset()
    keys = event.getKeys(keyList=[start_key, end_key], timeStamped=keys_clock)

    for key, rt in keys:
        if key == start_key:
            break
        elif key == end_key:
            win.close()
            core.quit()
    else:
        continue
    break
        
mouse = event.Mouse()

#Main loop
while len(mainstack):
    
    trial = [] # initialize a trial data list

    # Render the top card of the stack
    mainstack.render()
    
    # Render top card of discard stack and the corresponding stimcards
    for stack in dstacks.values():
        stack.render()
          

    # Update window
    win.flip()
    
    choice = None
    keys_clock.reset()
    while choice is None:
        # Check for mouse click first
        if mouse.getPressed()[0]:  # [0] corresponds to the left mouse button
            mouse_pos = mouse.getPos()
            for i, dstack in dstacks.items():
                rect = dstack.stimulus_card.rect
                if (rect[0] <= mouse_pos[0] <= rect[2] and rect[1] >= mouse_pos[1] >= rect[3]): #left,top,right,bottom
                    choice = i
                    break
        else:
            # If no mouse click, wait for keyboard input
            keys = event.getKeys(keyList=['1','2','3','4', 'escape'], timeStamped=keys_clock)
            for key, rt in keys:
                if key == 'escape':
                    win.close()
                    core.quit()
                elif key in ['1', '2', '3', '4']:
                    choice = int(key)
                    track(rt, trial)

    # Pop the top card from the mainstack and put it in the right discard pile
    card = mainstack.pop()
    track(card.__repr__(),trial)
    
    dstacks[choice].add(card)
    track(dstacks[choice].stimulus_card.__repr__(),trial)
    

    
    # Feedback
    chosen_card=dstacks[choice].stimulus_card
    correct = card.get_card_property(active_rule)==chosen_card.get_card_property(active_rule)
    track(correct,trial)
    
    if correct:
        win_music.stop()
        win_music.play()
        win_streak += 1 
        text = visual.TextStim(win, **success)
        text.draw()
    else:
        win_streak = 0
        text = visual.TextStim(win, **fail)
        text.draw()
        
    # Logg results
    match = matched_category(rules, choice, card, chosen_card)
    track(match,trial)
    track(active_rule,trial)
    track(win_streak,trial)
    # Change rule if streak is more than 5   
    if win_streak >= 5:
        active_rule=random.choice(list(set(rules).difference([active_rule])))
        win_streak = 0
    
    game_data.append(trial)
    # print(game_data)

# Data analysis for end screen
p, c, e = results(game_data)
pro = int(p)
log_message = f"You got a total of {pro}% correct. You completed a total of {c} categories. Preservative errors: {e}"
logging.log(level=logging.DATA, msg=log_message)

save_results(game_data, filename)

#End screen
win.flip(clearBuffer=True)
results = visual.TextStim(win, font=font, pos=(0, 0), height=30, ori=0.0, color='black', colorSpace='rgb', opacity=None, languageStyle='LTR', depth=0.0,
                          text=f"{summary_text_list[0]} {pro}% \n {summary_text_list[1]} {c} \n {summary_text_list[2]} {e}") # show some score data at the end of the game.
results.draw()
win.flip()
core.wait(8)

# End of task message
Goodbye_text = visual.TextStim(win, text=Goodbyetext, alignHoriz='center', alignVert='center',
                           font=font, pos=(0, 0), height=30,  ori=0.0,
                           color='black', colorSpace='rgb', opacity=None, languageStyle='LTR', depth=0.0)
Goodbye_text.draw()
win.flip()
keys = event.waitKeys(keyList=['space'])
win.close()

# core.quit()
