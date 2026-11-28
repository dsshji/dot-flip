# dot-flip
Dot flip display that plays the music with the mechanical clicks

digital prototype on p5: 
- [preview](https://editor.p5js.org/dsshji/full/OJB_bCk_a) 
- [code](https://editor.p5js.org/dsshji/sketches/OJB_bCk_a) 

click sound synthesized to imitate real, full structure ready on p5.js

jumping from one frequency to another --> pen that draws across the board (both rows and columns) using Bresenham's line algorithm (wow)

thickness depends on lowness, length on the velocity, positioning on the frequency

DS1 switches [4, 3, 1, 2] 
(top to bottom)
B1 OFF OFF ON OFF OFF OFF OFF OFF
B2 ON ON OFF OFF OFF OFF OFF OFF
B3 ON OFF OFF OFF OFF OFF OFF OFF
B4 OFF ON OFF OFF OFF OFF OFF OFF

sound files (Persona Playlist):
- [Rivers In The Desert (Persona 5)](https://onlinesequencer.net/3984214#)
- [It's Going Down Now (Persona 3 Reload)](https://onlinesequencer.net/3966309) 
- [Last Surprise (Persona 5)](https://onlinesequencer.net/4203312#)
- [Beneath The Mask (Persona 5)](https://onlinesequencer.net/3942363#)  
- [A Way Of Life (Persona 3 Portable)](https://onlinesequencer.net/4682602#) 
- [Color Your Night (Persona 3 Reload)](https://onlinesequencer.net/4018514#)
- [Full Moon Full Life (Persona 3 Reload)](https://onlinesequencer.net/4368919#) 
- [Heaven (Persona 4) ](https://onlinesequencer.net/4142018#)
- [Persona 3 Reload - When the Moon's Reaching Out Stars](https://onlinesequencer.net/4211463) 
- [Pull The Trigger (Persona Q2_ New Cinema Labyrinth)](https://onlinesequencer.net/4317522#) 
- [Take Over (Persona 5 Royal)](https://onlinesequencer.net/4086750#)
- [Wake Up, Get Up, Get Out There (Persona 5)](https://onlinesequencer.net/4040829#)


IT WORKSSSSSSSSSSSSSS
add troubleshooting for bord being plugged / unplugged

TODO:
- plug / unplug code handling (start from the last started song + add tracking of songs)
- RPi connect (Raspberry Pi 3 B+)
- how to play audio on Rpi?
- aux cable to RPi + speaker; RPi microSD card + laptop code

sound.py is done by Claude to play notes on Windows / Linux
else is me