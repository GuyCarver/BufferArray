# Sublime Text BufferArray Package

## Install

    $ https://github.com/GuyCarver/BufferArray

## Instructions

### Settings:

* MaxSlots = 10 by default.
* Slots = A list of tuples of (row, view.file_name() or view.name()) with a length of MaxSlots.

The settings are saved after buffer save.
The setting will be written to User/BufferArray.sublime-settings

### Key Bindings:

I have bound the 10 slots to they Keypad numbers.
* ctrl+keypad[0-9] will set the current view into the requisite slot.
* ctrl+K, keypad[0-9] will set the current view into the requisite slot as well as the current row.

* keypad[0-9] will set the active view to the view stored in that slot.  If the file is not open it will be opened.  If a row index > 0 was set the cursor will be placed on that row.
* If row < 0 then the the name is a view.name() and the view is most likely a scratch view with no file name.
