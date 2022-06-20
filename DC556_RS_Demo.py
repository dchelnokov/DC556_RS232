import os
import sys
import time

codes = {   'zoom in key down'                      : "52,0B,04,01,00,A1,01,04",
            'zoom in key up'                        : "52,0B,04,01,00,A1,00,03",
            'zoom out key down'                     : "52,0B,04,01,00,A2,01,05",
            'zoom out key up'                       : "52,0B,04,01,00,A2,00,04",
            'auto focus key down'                   : "52,0B,04,01,00,A5,01,08",
            'auto focus key up'                     : "52,0B,04,01,00,A5,00,07",
            'highlight key down'                    : "52,0B,04,01,00,B6,01,19",
            'highlight key up'                      : "52,0B,04,01,00,B6,00,18",
            'RECORDING Key Down'.lower()            : "52,0B,04,01,00,AC,01,0F",
            'RECORDING Key Up'.lower()              : "52,0B,04,01,00,AC,00,0E",
            'PLAYBACK Key Down'.lower()             : "52,0B,04,01,00,AE,01,11",
            'PLAYBACK Key Up'.lower()               : "52,0B,04,01,00,AE,00,10",
            'BRIGHTNESS Key Down'.lower()           : "52,0B,04,01,00,BD,01,20",
            'BRIGHTNESS Key Up'.lower()             : "52,0B,04,01,00,BD,00,1F",
            'FREEZE Key Down'.lower()               : "52,0B,04,01,00,B3,01,16",
            'FREEZE Key Up'.lower()                 : "52,0B,04,01,00,B3,00,15",
            'ICON Key Down'.lower()                 : "52,0B,04,01,00,AF,01,12",
            'ICON Key Up'.lower()                   : "52,0B,04,01,00,AF,00,11",
            'MENU Key Down'.lower()                 : "52,0B,04,01,00,AA,01,0D",
            'MENU Key Up'.lower()                   : "52,0B,04,01,00,AA,00,0C",
            'FLIP Key Down'.lower()                 : "52,0B,04,01,00,B2,01,15",
            'FLIP Key Up'.lower()                   : "52,0B,04,01,00,B2,00,14",
            'UP Key Down'.lower()                   : "52,0B,04,01,00,A6,01,09",
            'UP Key Up'.lower()                     : "52,0B,04,01,00,A6,00,08",
            'DOWN Key Down'.lower()                 : "52,0B,04,01,00,A7,01,0A",
            'DOWN Key Up'.lower()                   : "52,0B,04,01,00,A7,00,09",
            'LEFT Key Down'.lower()                 : "52,0B,04,01,00,A8,01,0B",
            'LEFT Key Up'.lower()                   : "52,0B,04,01,00,A8,00,0A",
            'RIGHT Key Down'.lower()                : "52,0B,04,01,00,A9,01,0C",
            'RIGHT Key Up'.lower()                  : "52,0B,04,01,00,A9,00,0B",
            'OK Key Down'.lower()                   : "52,0B,04,01,00,AB,01,0E",
            'OK Key Up'.lower()                     : "52,0B,04,01,00,AB,00,0C",
            'MANUAL FOCUS OUT Key Down'.lower()     : "52,0B,04,01,00,B9,01,1C",
            'MANUAL FOCUS OUT Key Up'.lower()       : "52,0B,04,01,00,B9,00,1B",
            'MANUAL FOCUS IN Key Down'.lower()      : "52,0B,04,01,00,BA,01,1D",
            'MANUAL FOCUS IN Key Up'.lower()        : "52,0B,04,01,00,BA,00,1C",
            'QUICKZOOM 2X Key Down'.lower()         : "52,0B,04,01,00,A3,01,06",
            'QUICKZOOM 2X Key Up'.lower()           : "52,0B,04,01,00,A3,00,05",
            'MASK Key Down'.lower()                 : "52,0B,04,01,00,B5,01,18",
            'MASK Key Up'.lower()                   : "52,0B,04,01,00,B5,00,17",
            'MACRO Key Down'.lower()                : "52,0B,04,01,00,A4,01,07",
            'MACRO Key Up'.lower()                  : "52,0B,04,01,00,A4,00,06",
            'SIZE Key Down'.lower()                 : "52,0B,04,01,00,B7,01,1A",
            'SIZE Key Up'.lower()                   : "52,0B,04,01,00,B7,00,19",
            'COLOR Key Down'.lower()                : "52,0B,04,01,00,B8,01,1B",
            'COLOR Key Up'.lower()                  : "52,0B,04,01,00,B8,00,1A",
            'VOLUME UP Key Down'.lower()            : "52,0B,04,01,00,B0,01,13",
            'VOLUME UP Key Up'.lower()              : "52,0B,04,01,00,B0,00,12",
            'VOLUME DOWN Key Down'.lower()          : "52,0B,04,01,00,B1,01,14",
            'VOLUME DOWN Key Up'.lower()            : "52,0B,04,01,00,B1,00,13",
            'PIP Key Down'.lower()                  : "52,0B,04,01,00,B4,01,17",
            'PIP Key Up'.lower()                    : "52,0B,04,01,00,B4,00,16",
            'Effect Graphics'.lower()               : "52,0B,04,40,01,01,00,A3",
            'Effect Text'.lower()                   : "52,0B,04,40,01,01,01,A4",
            'Effect B&W'.lower()                    : "52,0B,04,40,01,01,02,A5",
            'Effect Negative'.lower()               : "52,0B,04,40,01,01,03,A6",
            'Effect Sketch'.lower()                 : "52,0B,04,40,01,01,04,A7",
            'Image Size 0.8M'.lower()               : "52,0B,04,40,01,03,00,A5",
            'Image Size 2M'.lower()                 : "52,0B,04,40,01,03,01,A6",
            'Image Size 5M'.lower()                 : "52,0B,04,40,01,03,02,A7",
            'Video Mode HQ'.lower()                 : "52,0B,04,40,01,04,01,A6",
            'Video Mode HFR'.lower()                : "52,0B,04,40,01,04,01,A7",
            'LED Lamp'.lower()                      : "52,0A,04,70,00,12,FF,E1",

            
    }

def emulate_key(key_name, duration=0.05):
    """
    sends up and down key command for a duration of seconds
    key_name - string
    duration - float
    returns 0
    """
    duration = abs(duration)
    print(f'\n  sending {key_name} for {duration} sec.')
    # check if the command is found
    down = True if (key_name.lower() + ' key down') in codes.keys() else False
    up = True if (key_name.lower() + ' key up') in codes.keys() else False
    if not down:
        print(f'command "{key_name}" not found')
        return 0
    else:
        cmd_dwn = codes[key_name + ' key down']
    print(f"sending codes {key_name} as {cmd_dwn}. ")
    r = tx_hex(ser, to_b_sequence(cmd_dwn.split(sep=',')))
    print(f'Response: {r}')
    
    if up:
        cmd_up = codes[key_name.lower() + ' key up']
        ending = '' if duration <=1 else 's'
        if duration > 1:
            print(f'preparing to send key release - waiting {duration} second{ending}...')
        time.sleep(duration)   # full zo out time
        print('sending key release')
        r = tx_hex(ser, to_b_sequence(cmd_up.split(sep=',')))
        print(f'Response: {r}')
    return r

try:
    os.chdir(r'C:\Users\DXC\AppData\Roaming\Python\Python39\Scripts')
except:
    pass
import serial

def to_b_sequence(hex_string):
    """
    takes a list of str representing hex bytes ['AA', '9D']...
    returns a bytearray with each item of 1 byte
    """
    print(f'got the string {hex_string}')
    result = bytearray()
    for i in hex_string:
        if len(i) < 2:
            while len(i) < 2:
                i = '0' + i
        try:
            # print(f'part {i}')
            hex_int = int((i[-2:]), 16)
        except:
            print(f'Error when converting {i} to integer...')
            sys.exit()
        result.append(hex_int)
    return result

def tx_hex(handler, cmd):
    """
       takes handler as PySerial object
       takes cmd as a bytearray
           sends bytes to the handler
        returns response, if any
    """
    feedback = []
    try:
        msg_to_send = cmd
        # print(f'>sending {msg_to_send}')
        handler.write(msg_to_send)
        
        # getting response:
        b = handler.read()
        while b:
            feedback.append(b)
            b = handler.read()
        
    except:
        print(f"Couldn't send the command. ")
    f = []

    for i in feedback:
        f.append(i.hex())
    feedback = (','.join(f)).upper()
        
            
    return feedback
            
def tx_cmd(handler, cmd):
    # sends ASCII, returns ASCII
    feedback = ''
    try:
        msg_to_send = cmd + '\r'
        print(f'>sending {msg_to_send}')
        handler.write(msg_to_send.encode())
        # getting response:
        b = handler.read()
        while b:
            feedback += b.decode()
            b = handler.read()
    except:
        print(f"Couldn't send the command {cmd}.")
    return feedback

def full_zoom_out(ser):
    print('FULL ZOOM OUT')
    # full zoom out
    print(f"sending codes['zoom out key down'] as {codes['zoom out key down']}. ")
    r = tx_hex(ser, to_b_sequence(codes['zoom out key down'].split(sep=',')))
    print(f'Response: {r}')
    print('preparing to send key release')
    time.sleep(11.5)   # full zoom out time
    print('sending key release')
    r = tx_hex(ser, to_b_sequence(codes['zoom out key up'].split(sep=',')))
    print(f'Response: {r}')
    r = tx_hex(ser, to_b_sequence(codes['zoom out key up'].split(sep=',')))
    print(f'Response: {r}')

def zoom_in(ser, seconds):
    print(f'ZOOM IN {seconds} seconds deep')
    print(f"sending codes['zoom in key down'] as {codes['zoom in key down']}. ")
    
    r = tx_hex(ser, to_b_sequence(codes['zoom in key down'].split(sep=',')))
    print(f'Response: {r}')
    
    print(f'preparing to send key release in {seconds} seconds')
    time.sleep(seconds)   # full zoom out time
    print('sending key release')
    r = tx_hex(ser, to_b_sequence(codes['zoom in key up'].split(sep=',')))
    print(f'Response: {r}')

def zoom_out(ser, seconds):
    print(f'ZOOM OUT {seconds} seconds deep')
    print(f"sending codes['zoom out key down'] as {codes['zoom out key down']}. ")
    r = tx_hex(ser, to_b_sequence(codes['zoom out key down'].split(sep=',')))
    print(f'Response: {r}')
    print(f'preparing to send key release in {seconds} seconds')
    time.sleep(seconds)   # full zoom out time
    print('sending key release')
    r = tx_hex(ser, to_b_sequence(codes['zoom out key up'].split(sep=',')))
    print(f'Response: {r}')

argv = sys.argv  # ['DC556_RS_Demo', 'COM5']
arg_len = len(sys.argv)
delay = 0.2 
port=''
commands = []
demo = False
total_shows = 500  # for about 4 hours 
     
if arg_len > 2:
    port = sys.argv[1]
    for itm in sys.argv[2:]:
        if itm.lower() in codes.keys():  #
            commands.append(codes[itm.lower()].split(sep=','))  #
        else:  #
            commands.append(itm.split(sep= ',' if ',' in itm else ' '))
elif (arg_len > 1 and sys.argv[1] in ('help', '?', r'/?', 'h', '-h', '--help')):
    print(f' Not enough arguments: expected 2 or more, received {arg_len}',
          '\n\n Tip: The first argument is the port name (e.g. "COM5"), than one or more commands that must be sent\n',
          r' Example: C:\DC556_serial_demo.exe "COM5" "52 0A 04 70 00 12 FF" "52 0A 04 70 00 12 FF"',
          
          f"\n  Each next command in the line will be sent with {delay} second{'s' if delay > 1 else ''} delay.",
          "\n  After sending each command the response from host will be shown - if any.",
          "\n *Please send bug reports to 2chelnokov@gmail.com with the keyword 'bug_report' in subject",
          "\n (c) Dmitry Chelnokov 2022")
    sys.exit()
elif arg_len > 1:
    port = sys.argv[1]
    print(f'Automatic mode on port {port}')
    demo = True
else:
    print(f'No arguments found. Please run {sys.argv[0]} -h for help')
    sys.exit()

    
try:
    print(f'>Opening connection to {port}...')
    ser = serial.Serial(port=port,
                        baudrate=9600,
                        parity=serial.PARITY_NONE,
                        bytesize=8,
                        timeout=0,
                        xonxoff=False,
                        stopbits=serial.STOPBITS_ONE
                        )
except:
    print(f"Error: can't open the serial port '{port}':", )
    sys.exit()
if not demo:
    for cmd in commands:
        r = tx_hex(ser, to_b_sequence(cmd))
        print(f"> Response for {cmd} was:\n{r if r and len(r) else 'No response'}")
        
        if arg_len > 3:
            print(f"> wait {delay} second{'s' if delay > 1 else ''}")
            time.sleep(delay)
else:
    times = 0

    full_zoom_out(ser)
    time.sleep(1)
    zoom_in(ser, 1)
    print('starting main scenario... ')
    time_to_zoom_in = 5  # 11.4 is enough for maximal zoom in
    time_in_zoomed_picture = 5
    time_to_zoom_out = 6
    time_in_zoomed_out_pic = 10
    time.sleep(2)
    h_seq = ['highlight']
    #h_seq.extend(['left'] * 3)
    h_seq.extend(['up'] * 4)
    h_seq.extend(['left'] * 8)
    h_seq.extend(['down'] * 4)
    h_seq.extend(['right'] * 8)
    h_seq.extend(['highlight'])
        
    while times < total_shows:
        print(f'cycle #{times}')
        
        
        for button in h_seq:
            emulate_key(button, 0.5)
            time.sleep(0.15)
        
        if (not times / 50) and times > 2:
            print(f'The show performing FULL ZOOM OUT #{times}\n')
            full_zoom_out()

        print('ZOOMING IN!')    
        zoom_in(ser, time_to_zoom_in)
        # wait
        print(f'... waiting {time_in_zoomed_picture} seconds before zooming OUT')
        time.sleep(time_in_zoomed_picture)
        
        zoom_out(ser, time_to_zoom_out)
        print(f'... waiting {time_in_zoomed_out_pic} seconds..')
        time.sleep(time_in_zoomed_out_pic)
        times += 1
    print(f'Program fired {times} times and will now exit')
        
        
 

ser.close()
print('<< END.')



