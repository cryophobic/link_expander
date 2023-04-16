# Adding all the non-essential, but useful functions here

import time

cursor_chars = ['|', '/', '-', '\\']


# A little load animation to let users know something is happening

def load_anim(stop_event):
    while not stop_event.is_set():
        for cursor in '|/-\\':
            print('Expanding URLs ' + cursor, end='\r')
            time.sleep(0.1)
    print('\r', end='')
    