import turtle
import threading



wn = turtle.Screen()
smiles = turtle.Turtle()
emotionG = None
moistureLevelG = 0
temperatureG = 0.00
timesPerWeekG = 0
wateringForG = 0
countdownG = None
buttonPressedG= 0


#This updates the firebase database with input from stemma
def databaseUpdate():
    import firebase
    from firebase.firebase import FirebaseApplication
    firebase = firebase.firebase.FirebaseApplication("https://plantsystem-1e4fa.firebaseio.com", None)
    firebase.put('MainUser',
                 "Moisture", moistureLevelG)
    firebase.put('MainUser',
                 "Temperature", temperatureG)
    firebase.put('MainUser',
                 "Emotion", emotionG)
    firebase.put('MainUser',
                 "SetHoursBetweenWatering", timesPerWeekG)
    firebase.put('MainUser',
                 "Countdown", countdownG)








def countdown(h=0):  # this countdown method got inspiration from https://stackoverflow.com/questions/28036587/python-3-4-timer-count-down-not-working
    from datetime import datetime, timedelta
    import time
    print("Counting")
    update = True
    counter = timedelta(hours=h)
    while counter:
        time.sleep(1)
        counter -= timedelta(seconds=1)
        if counter ==0:
            motorGo()
        print("Time remaining: {}".format(counter))
        global countdownG
        countdownG = counter  # DO THIS FOR GLOBAL VAR
        if counter.seconds == 86400:
            update = True

        if update:
            databaseUpdate()  # DO NOT REMOVE
            update = False




def stemmaGo():
  #  t2 = threading.Thread(target=test)
  #  t2.start()
    t1 = threading.Thread(target=countdown, args=(1,))
    t1.start()
    test()



def test():
    while True:
        """
        import RPi.GPIO as GPIO
        import time

        from board import SCL, SDA
        import busio

        from adafruit_seesaw.seesaw import Seesaw

        i2c_bus = busio.I2C(SCL, SDA)

        ss = Seesaw(i2c_bus, addr=0x36)
        """
        print("Stemma: Checking moisture and temp")
        #read moisture level through capacitive touch pad
#        touch = ss.moisture_read()
        touch = 676 #delete THIS

        global moistureLevelG
        moistureLevelG = touch
        #read temperature from the temperature sensor
        #temp = ss.get_temp()
        temp = 77 #Delete this


        farenh = int(temp) * 9 / 5 + 32
        global temperatureG
        temperatureG = farenh

        databaseUpdate()
        import firebase
        from firebase.firebase import FirebaseApplication
        firebase = firebase.firebase.FirebaseApplication("https://plantsystem-1e4fa.firebaseio.com", None)
        global buttonPressedG
        buttonPressedG = firebase.get('MainUser','ButtonPressed')
        print("Button Pressed: " + str(buttonPressedG))
        if buttonPressedG ==1:
            motorGo()
        emotionCheck()#DO NOT REMOVE
        databaseUpdate()#DO NOT REMOVE

#Starts motor and runs according to plant size
def motorGo():
    #import RPi.GPIO as GPIO
    import time
    #GPIO.setmode(GPIO.BCM)

    # motor functions
    Motor1A = 23  # gpio out pin 16
    Motor1B = 24  # gpio in pin 18
    Motor1E = 25  # enable- provide power to base of transistor.
    # eg which can be manipulated before gpio out. pin 22

    GPIO.setup(Motor1A, GPIO.OUT)
    GPIO.setup(Motor1B, GPIO.OUT)
    GPIO.setup(Motor1E, GPIO.OUT)


    print("Turning motor on")
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor1E, GPIO.HIGH)

    print("Motor watering for: " + str(wateringForG))
    time.sleep(wateringForG)



    print("Stopping motor")
    GPIO.output(Motor1E, GPIO.LOW)
    print("clean up")
    GPIO.cleanup()

    #watering = 0 eg false on firebase
    import firebase
    from firebase.firebase import FirebaseApplication
    firebase = firebase.firebase.FirebaseApplication("https://plantsystem-1e4fa.firebaseio.com", None)
    firebase.put('MainUser',
                 "ButtonPressed", 0)
    databaseUpdate()
    print("Motor turning off.")
    









#This activates graphic for happy face
def happy():
    turtle.hideturtle()
    turtle.bgcolor("green")

    turtle.up()
    turtle.goto(0, -100)  # head in center

    turtle.begin_fill()
    turtle.fillcolor("yellow")
    turtle.circle(100)
    turtle.end_fill() #Fill the shape drawn after the last call to begin_fill().

    turtle.up()
    turtle.goto(-67, -40)
    turtle.setheading(-60)
    turtle.width(5)
    turtle.down()
    turtle.circle(80, 120)  #

    turtle.fillcolor("black")

    for i in range(-35, 105, 70):
        turtle.up()
        turtle.goto(i, 35)
        turtle.setheading(0)
        turtle.down()
        turtle.begin_fill()
        turtle.circle(10)  # draw eyes
        turtle.end_fill()

#This activates graphic for sad face
def sad():
    turtle.hideturtle()
    turtle.bgcolor("red")


    turtle.up()
    turtle.goto(0, -100)  # center circle around origin


    turtle.begin_fill()
    turtle.fillcolor("yellow")  # draw head
    turtle.circle(100)
    turtle.end_fill() #Fill the shape drawn after the last call to begin_fill().

    turtle.up()
    turtle.goto(67, -40) #x,y coord.
    turtle.setheading(-60)
    turtle.width(5)
    turtle.down()
    turtle.circle(-80, -120)  # draw smile

    turtle.fillcolor("black")

    for i in range(-35, 105, 70):
        turtle.up()
        turtle.goto(i, 35)
        turtle.setheading(0)
        turtle.down()
        turtle.begin_fill()
        turtle.circle(10)  # draw eyes
        turtle.end_fill()







def emotionCheck():
    print("EmotionCheck: Checking emotion")
    if moistureLevelG >= 450 and moistureLevelG <= 830:
        emotion1 = "Happy"
        happy()  # show on this display
        global emotionG
        emotionG = emotion1


    elif moistureLevelG < 450 or moistureLevelG > 830:
        emotion2 = "Sad"
        emotionG = emotion2
        sad()  # show on this display



def plantOptions():
    global timesPerWeekG
    global wateringForG

    waterOption = input(
        "How many times a week would you like to water your plant?\nOPTION [1]: Every other day \nOPTION [2]: Twice a week \nOPTION [3]: Once a week\nType: ")

    if waterOption == "1":
        print("You chose water every other day.\n")
        timesPerWeekG = 48  # Every other day
        waterAmount = input("How big is the plant? \nOPTION [1]: small\nOPTION [2]: medium\nOPTION [3]: large\nType: ")
        if (waterAmount == "1"):
            wateringForG = 15
            print("You chose: Small plant" + "Water for: " + str(wateringForG))
            print("You're all set!")
        elif (waterAmount == "2"):
            wateringForG = 30
            print("You chose: Medium plant" + "Water for: " + str(wateringForG))
            print("You're all set!")
        elif (waterAmount == "3"):
            wateringForG = 60
            print("You chose: Large plant" + "Water for: " + str(wateringForG))
            print("You're all set!")
        else:
            print("Error: Wrong Entry")

    elif waterOption == "2":
        print("You chose water twice a week.\n")
        timesPerWeekG = 84  # twice a week
        waterAmount = input("How big is the plant? \nOPTION [1]: small\nOPTION [2]: medium\nOPTION [3]: large\nType: ")
        if (waterAmount == "1"):
            wateringForG = 15
            print("You chose: Small plant" + "Water for: " + str(wateringForG))
            print("You're all set!")
        elif (waterAmount == "2"):
            wateringForG = 30
            print("You chose: Medium plant" + "Water for: " + str(wateringForG))
            print("You're all set!")
        elif (waterAmount == "3"):
            wateringForG = 60
            print("You chose: Large plant" + "Water for: " + str(wateringForG))
            print("You're all set!")
        else:
            print("Error: Wrong Entry")

    elif waterOption == "3":
        print("You chose water once a week.\n")
        timesPerWeekG = 168  # once a week
        waterAmount = input("How big is the plant? \nOPTION [1]: small\nOPTION [2]: medium\nOPTION [3]: large\nType: ")
        if (waterAmount == "1"):
            wateringForG = 15
            print("You chose: Small plant" + "Water for: " + str(wateringForG))
            print("You're all set!")
        elif (waterAmount == "2"):
            wateringForG = 30
            print("You chose: Medium plant" + "Water for: " + str(wateringForG))
            print("You're all set!")
        elif (waterAmount == "3"):
            wateringForG = 60
            print("You chose: Large plant" + "Water for: " + str(wateringForG))
            print("You're all set!")
    else:
        print("Error: Wrong entry")
    stemmaGo()




plantOptions()






#have two functions one for counter and one for the process


