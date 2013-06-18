# Sublime Text BufferArray Package

## Install

    $ https://github.com/GuyCarver/BufferArray

## Instructions

### Settings:

* MaxSlots = 10 by default.
* Slots = A list of tuples of (view.name(), view.file_name()) with a length of MaxSlots.

The settings are saved after buffer save.
The setting will be written to User/BufferArray.sublime-settings

### Key Bindings:

I have bound the 10 slots to they Keypad numbers.
* ctrl+keypad[0-9] will set the current view into the requisite slot.

* keypad[0-9] will set the active view to the view stored in that slot.  If the file is not open it will be opened.
