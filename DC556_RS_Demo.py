import os
import sys
import time

codes = {   'zoom in key down'      : "52,0B,04,01,00,A1,01,04",
            'zoom in key up'        : "52,0B,04,01,00,A1,00,03",
            'zoom out key down'     : "52,0B,04,01,00,A2,01,05",
            'zoom out key up'       : "52,0B,04,01,00,A2,00,04",
            'auto focus key down'   : "52,0B,04,01,00,A5,01,08",
            'auto focus key up'     : "52,0B,04,01,00,A5,00,07",
    }

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
delay = 0.3 
port=''
commands = []
demo = False
total_shows = 150  # for about 4 hours 
     
if arg_len > 2:
    port = sys.argv[1]
    for itm in sys.argv[2:]:
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
    time_to_zoom_in = 4  # 11.4 is enough for maximal zoom in
    time_in_zoomed_picture = 60
    time_to_zoom_out = 4
    time_in_zoomed_out_pic = 30
    
    while times < total_shows:
        print(f'cycle #{times}')
        
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



