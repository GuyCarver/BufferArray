import sublime, sublime_plugin
import os

sets_path = "BufferArray.sublime-settings"
ba_settings = None
buf = None

class Buffers :
  def __init__( self ) :
    self.Dirty = False
    self.Slots = [(-3, "")] * ba_settings.get("MaxSlots", 10)
    sl = ba_settings.get("slots")
    if sl :
      i = 0
      for s in sl :
        if i < len(self.Slots) :
          self.Slots[i] = s
          i += 1

  def Set( self, aSlot, aName, aPath, aRow ) :
    if aPath :
      sname = aPath
    else :
      aRow = -1
      sname = aName if aName else ""

    self.Slots[aSlot] = (aRow, sname)
    self.Dirty = True
#    print("setting slot {}: {}".format(aSlot, self.Slots[aSlot]))

  def Get( self, aSlot ) :
#    print("getting slot {}: {}".format(aSlot, self.Slots[aSlot]))
    return self.Slots[aSlot]

  def List( self ) :
    i = 0
    for b in self.Slots :
      print("{}: {}".format(i, b))
      i += 1

  def _GetDisplayName( self, aSlot ) :
    return aSlot

  def GetItems( self ) :
    def nameString(aSlot) :
      _, name = os.path.split(aSlot[1])
      if aSlot[0] > 0 :
        name += ":" + str(aSlot[0])
      return name

    return [nameString(slot) for slot in self.Slots ]

  def getScratch( self, aWindow, aName ) :
    for v in aWindow.views() :
#      print("Comparing: {} - {}".format(aName, v.name()))
      if v.name() == aName :
        aWindow.focus_view(v)
        break

  def SetActive( self, aWindow, aSlot ) :
    t, p = buf.Get(aSlot)
    if t >= 0 :
      if t > 0 :
        openF = sublime.ENCODED_POSITION
        p = p + ':' + str(t)
      else:
        openF = 0
      vw = aWindow.open_file(p, openF)
      if vw :
#        print("setting focus to " + p)
        g, i = aWindow.get_view_index(vw)
        aWindow.focus_view(vw)
        aWindow.focus_group(g)
    else:
      self.getScratch(aWindow, p)

  def Save( self ) :
    if self.Dirty :
      ba_settings.set("slots", self.Slots)
      sublime.save_settings(sets_path)
      self.Dirty = False

class SetBufferCommand( sublime_plugin.WindowCommand ) :
  def run( self, slot, row = False ) :
    vw = self.window.active_view()

    if row :
      print("row set")
      pnt = vw.sel()[0].a
      vrow, _ = vw.rowcol(pnt)
      vrow += 1 #1 based.
    else:
      vrow = 0
    buf.Set(slot, vw.name(), vw.file_name(), vrow)

class GetBufferCommand( sublime_plugin.WindowCommand ) :

  def run( self, slot ) :
    buf.SetActive(self.window, slot)

class ListBuffersCommand( sublime_plugin.WindowCommand ) :
  def run( self ) :
    buf.List()

class GotoBufferCommand( sublime_plugin.WindowCommand ) :
  def run( self ) :
    win = sublime.active_window()
    win.show_quick_panel(self.get_items(), self.select)

  def select( self, aIndex ) :
    if aIndex != -1 :
      buf.SetActive(self.window, aIndex)

  def get_items( self ) :
    return buf.GetItems()

class BufferListener( sublime_plugin.EventListener ) :
  def on_post_save_async( self, view ) :
    buf.Save()

def plugin_loaded(  ) :
  global buf
  global ba_settings

  ba_settings = sublime.load_settings(sets_path)
  buf = Buffers()