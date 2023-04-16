# Adding all the non-essential, but useful functions here

import time

cursor_chars = ['|', '/', '-', '\\']


# A little load animation to let users know something is happening
def load_anim():
    while True:
        for cursor_char in cursor_chars:
            print(f'\rProcessing... {cursor_char}', end='', flush=True)
            time.sleep(0.1)