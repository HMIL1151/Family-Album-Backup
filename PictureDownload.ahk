#Persistent
CoordMode, Mouse, Screen
SetTimer, DoMacro, 1000 ; Run the macro every second
return

^Esc::ExitApp ; Press CTRL + ESC to exit the script

DoMacro:
    ; Click and drag from (X1, Y1) to (X2, Y2)
    X1 := 1900
    Y1 := 510
    X2 := 1530
    Y2 := 510
    
    MouseMove, %X1%, %Y1% ; Move to starting point
    Sleep, 50            ; Pause briefly
    Click, Down           ; Press and hold the left mouse button
    MouseMove, %X2%, %Y2%, 10 ; Drag to the end point (with speed)
    Sleep, 50            ; Pause briefly
    Click, Up             ; Release the mouse button
    
    ; Perform two clicks
    Click, 1892, 124 ; First click at (1890, 124)
    Sleep, 200       ; Pause briefly
    Click, 1730, 175 ; Second click at (1719, 169)
return
