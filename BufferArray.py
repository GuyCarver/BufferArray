import sublime, sublime_plugin

sets_path = "BufferArray.sublime-settings"
ba_settings = sublime.load_settings(sets_path)

class Buffers :
  def __init__( self ) :
    self.Dirty = False
    self.Slots = [","] * ba_settings.get("MaxSlots", 10)
    sl = ba_settings.get("slots")
    if sl :
      i = 0
      for s in sl :
        if i < len(self.Slots) :
          self.Slots[i] = s
          i += 1

  def Set( self, aSlot, aName, aPath ) :
    if not aName :
      aName = ""
    if not aPath :
      aPath = ""

    self.Slots[aSlot] = aName + "," + aPath
    self.Dirty = True
#    print "setting slot %d: %s" % (aSlot, self.Slots[aSlot])

  def Get( self, aSlot ) :
#    print "getting slot %d: %s" % (aSlot, self.Slots[aSlot])
    return self.Slots[aSlot]

  def List( self ) :
    i = 0
    for b in self.Slots :
      print "%d: %s" % (i, b)
      i += 1

  def _GetDisplayName( self, aSlot ) :
    return aSlot

  def GetItems( self ) :
    return self.Slots #[self._GetDisplayName(slot) for slot in self.Slots ]

  def getScratch( self, aWindow, aName ) :
    for v in aWindow.views() :
#      print "Comparing: %s - %s" % (aName, v.name())
      if v.name() == aName :
        aWindow.focus_view(v)
        break

  def SetActive( self, aWindow, aSlot ) :
    n, p = buf.Get(aSlot).split(",", 1)
    if p and (p != "") :
      vw = aWindow.open_file(p)
      if vw :
#        print "setting focus to %s" % p
        g, i = aWindow.get_view_index(vw)
        aWindow.focus_view(vw)
        aWindow.focus_group(g)
    elif n and (n != "") :
      self.getScratch(aWindow, n)

  def Save( self ) :
    if self.Dirty :
      ba_settings.set("slots", self.Slots)
      sublime.save_settings(sets_path)
      self.Dirty = False

buf = Buffers()

class SetBufferCommand( sublime_plugin.WindowCommand ) :
  def run( self, slot ) :
    vw = self.window.active_view()
    buf.Set(slot, vw.name(), vw.file_name())

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
  def on_post_save( self, view ) :
    buf.Save()
