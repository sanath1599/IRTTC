import RPi.GPIO as GPIO              #Import GPIO Lib
import numpy                         #Import NumPy      
import cv2                           #Import Open CV
import sys                           #Import System
import Adafruit_DHT                  #Import Ada Fruit Library for the DHT11 Module
import time                          #Import Time Library for adding delay
import os                            #Import os for sending IR signals
GPIO.setmode(GPIO.BCM)               #Setup GPIO for BCM mode
GPIO.setup(4, GPIO.IN)               #Setup Pin 4 for DHT11 module input
GPIO.setup(17, GPIO.IN)              #Setup pin 17 for PIR

humidity, temperature = Adafruit_DHT.read_retry(11, 4) #Read Value of temperature and humidity
print 'Current Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity) #Print the above retreived values

if temperature >30:  #Temperature correction
        temperature=30

os.system('wget andromote.com/bosch/lircremotes.zip') #Download the latest remotes package from server
os.system('unzip lircremotes.zip') #Unzip it

"""The current code uses a if else loop to determine the brand and model of the remote,while a final version will
search the directory for a folder with the brand name and then copy lircd(n).conf file to the destination folder
and check for functionality,if yes=>Configured,if no n=n+1 for n in range."""
          
brand =input('Enter the AC Brand name:  ')  #AC Brand input    
if input==bosch:                          #If Bosch then
       
       os.system('mv -f bosch/lircd.conf /etc/lirc/lircd.conf ') #Test Bosch remote 1
       os.system('irsend SEND_ONCE ac on') #AC ON
       working =inpuut('Did it work') #Check if it worked
       if working==yes: #If yes
              print("Remote configured") #Then remote configured

       else:
              os.system('mv -f bosch/lircd1.conf /etc/lirc/lircd.conf ') #else Test Bosch remote 2 
              os.system('irsend SEND_ONCE ac on') #AC ON
              print("Remote configured") #configured

elif input==lg:
       os.system('mv -f lg/lircd.conf /etc/lirc/lircd.conf ') #Test LG remote 1
       os.system('irsend SEND_ONCE ac on') #AC ON
       working =inpuut('Did it work')
       if working==yes:
              print("Remote configured")

       else:
              os.system('mv -f lg/lircd1.conf /etc/lirc/lircd.conf ') #Test LG remote 2
              os.system('irsend SEND_ONCE ac on') #AC ON
              print("Remote configured")

else:
       print("Sorry remote not found,please wait while we add new brands to our database") #When remote not in database

time.sleep(3.5)
              
while True:
       humidity, temperature = Adafruit_DHT.read_retry(11, 4) #Read Value of temperature and humidity
      # print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity) 
       int= GPIO.input(17)
       if int==0: #If Motion
                print ("Motion Detected")
                print("Image analysis started")  #Fancy printing
        
                
                cam = VideoCapture(0)   # 0 -> index of camera
                s, img = cam.read()     #Read camera image     
                if s:    # frame captured without any errors
                    namedWindow("cam-test",CV_WINDOW_AUTOSIZE)
                    imshow("cam-test",img)
                    waitKey(0)
                    destroyWindow("cam-test")
                    imwrite("fn.jpg",img) #save image
                img = cv2.imread('fn.jpg') #read image from same directory
                average_color_per_row = numpy.average(img, axis=0) #find average of values per row
                average_color = numpy.average(average_color_per_row, axis=0) #find average of average
                average_color = numpy.uint8(average_color) #convert to unit8 format(integer from float) for convinience
                time.sleep(5) #Sleep to show that the program is heavy and took time
                print(average_color)       #print the RGB Values of the average color(Optional-will probably be removed for final)
                    
                print("Got the average color,Now finding the optimum temperature") #Fancy printing again
                time.sleep(2) 

                a=average_color #Allocating a to average_value for simplicity

                R=a.item(2) # allocating R,G & B Values 
                G=a.item(1)
                B=a.item(0)

                
                if R<5:          #logic part
                       if G<5:
                              if B<5:
                                     print("No Human detected,AC Off")
                                     os.system('irsend SEND_ONCE ac off') #AC OFF Because no human detected.
                
       
                if a.item(2)>a.item(1): #If ref is greater than green
                        if a.item(2)>a.item(0): #if red is greater than blue
                            gb=(G+B)/2
                            d=(R-gb)*10
                            td=d/R   
                            print("He's feeling HOT")#Print hot
                            opt=temperature-td
                            print(opt) #print "Optimum temperature"
                            os.system('irsend SEND_ONCE ac on') #AC ON
                            os.system('irsend SEND_ONCE ac ffast') #Fan speed high
                            os.system('irsend SEND_ONCE ac turbo') #Turn on turbo more
                            
                
                elif a.item(1)>a.item(0): #if green more than blue
                        if a.item(1)>a.item(2): #if green more than red
                            rb=(R+B)/2
                            d=(G-rb)*10
                            td=(d/G)/3  
                            print("It's not really hot or cold,He's Fine") #Print normal
                            if R>B :
                                 opt=temperature-td
                                 print(opt) #print room temperature -Temperature differnece
                                                 
                            else :
                                 opt=temperature+td  
                                 print(opt)
                            os.system('irsend SEND_ONCE ac on') #AC ON
                            os.system('irsend SEND_ONCE ac freg') #Fan speed regular
                        
                else: #For all other cases(only one though)
                            gr=(G+R)/2
                            d=(B-gr)*10
                            td=(d/B) #Temperature difference
                            print("he's feeling cold") #print again
                            opt=temperature+td
                            print(opt) #Print temp-5
                            os.system('irsend SEND_ONCE ac on') #AC ON
                            os.system('irsend SEND_ONCE ac flow') #Reduce fan speed

"""Fan swing on/off determination"""
                cam = VideoCapture(0)   # 0 -> index of camera
                s, img = cam.read()     #Read camera image     
                if s:    # frame captured without any errors
                    namedWindow("cam-test",CV_WINDOW_AUTOSIZE)
                    imshow("cam-test",img)
                    waitKey(0)
                    destroyWindow("cam-test")
                    imwrite("fn2.jpg",img) #save image (motion detection)
                img1 = cv2.imread('fn2.jpg') #read image from same directory
                average_color_per_row1 = numpy.average(img1, axis=0) #find average of values per row
                average_color1 = numpy.average(average_color_per_row1, axis=0) #find average of average
                average_color1 = numpy.uint8(average_color1) #convert to unit8 format(integer from float) for convinience
                time.sleep(5) #Sleep to show that the program is heavy and took time
                print("Intelligent real time motion detection" ,average_color1)
                R1=a.item(2) # allocating R,G & B Values 
                G1=a.item(1)
                B1=a.item(0)

                if ((R1-R)*100)/R > 10:  #If change in R> 10%
                       print("Motion found")
                       os.system('irsend SEND_ONCE ac SWINGon')
                       print("Turned on SWING") #Turn Swing on

                elif ((G1-G)*100)/G > 10: #If change in G> 10%
                       print("Motion found")
                       os.system('irsend SEND_ONCE ac SWINGon') #Turn Swing on
                       print("Turned on SWING")

                elif ((B1-B)*100)/B > 10: #If change in B> 10%
                       print("Motion found")
                       os.system('irsend SEND_ONCE ac SWINGon') #Turn Swing on
                       print("Turned on SWING")

                else:
                       print("No motion found")
                       os.system('irsend SEND_ONCE ac SWINGoff')
                       print("Turned off swing")
                       
                                


                
                if opt=16:                                     #IR Remote send part
                       os.system('irsend SEND_ONCE ac 16')
                elif opt=17:
                       os.system('irsend SEND_ONCE ac 17')
                elif opt=18:
                       os.system('irsend SEND_ONCE ac 18')
                elif opt=19:
                       os.system('irsend SEND_ONCE ac 19')

                elif opt=20:
                       os.system('irsend SEND_ONCE ac 20')
                elif opt=21:
                       os.system('irsend SEND_ONCE ac 21')
                elif opt=22:
                       os.system('irsend SEND_ONCE ac 22')
                elif opt=23:
                       os.system('irsend SEND_ONCE ac 23')
                elif opt=24:
                       os.system('irsend SEND_ONCE ac 24')
                elif opt=25:
                       os.system('irsend SEND_ONCE ac 25')

                elif opt=26:
                       os.system('irsend SEND_ONCE ac 26')
                elif opt=27:
                       os.system('irsend SEND_ONCE ac 27')
                elif opt=28:
                       os.system('irsend SEND_ONCE ac 28')
                elif opt=29:
                       os.system('irsend SEND_ONCE ac 29')
                elif opt=30:
                       os.system('irsend SEND_ONCE ac 30')

                print("Temperature successfully set") #Success in setting the intended optimum temperature
                
                else:
                       print("ERROR! TEMPERATURE OUT OF RANGE") #Error,temperature out of range
                time.sleep(300)#Delay and don't scan for 5 minutes.
       else:
                print ("No motion detected")



                


            
