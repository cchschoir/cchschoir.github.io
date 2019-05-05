import pygame, sys, subprocess, os, shutil, time
from pygame.locals import *

# Initialize Globals

# Format: [Score, Day]
daySeries = []
cSeries = [] # Callafiato is Orange
tSeries = [] # Teovedar is Purple
eSeries = [] # Ellazaire is Yellow
bSeries = [] # Baladeo is Blue
tickNum = 0
secNum = 0
dayNum = 0
pi = '/home/pi/Desktop/'
saveGame = False
reset = 11
def main():

    pygame.init()

    FPS = 30 # frames per second setting
    fpsClock = pygame.time.Clock()

    # set up the window
    
    w = 1280
    h = 1024
    
    pygame.display.set_caption('Choir House Points')

    global pi
    
    DISPLAYSURF = pygame.display.set_mode((w, h), pygame.RESIZABLE)

    try:
        backImg = pygame.image.load(pi +'back.png')
        pygame.mouse.set_visible(False)

    except pygame.error:
        print ('no images in first location')
        pi = ''
    backImg = pygame.image.load(pi + 'back.png')
    baseImg = pygame.image.load(pi + 'base.png')
    cImg = pygame.image.load(pi + 'barC.png')
    tImg = pygame.image.load(pi + 'barT.png')
    eImg = pygame.image.load(pi + 'barE.png')
    bImg = pygame.image.load(pi + 'barB.png')
    BASICFONT = pygame.font.Font(pi + 'GermaniaOne-Regular.ttf', 120)
    SMALLFONT = pygame.font.Font(pi + 'GermaniaOne-Regular.ttf', 10)

    # Initialize Variables

    global daySeries, cSeries, tSeries, eSeries, bSeries, tickNum, secNum, dayNum, saveGame, reset

    # **Retrieve previous scores from file

    # w/2 is middle of screen
    # -140 is middle of picture
    # number on end is offset of
    # the center of the bar from center of screen
    cLocX = w/2-140-450
    cLocY = h-200

    tLocX = w/2-140-150
    tLocY = h-200

    eLocX = w/2-140+150
    eLocY = h-200

    bLocX = w/2-140+450
    bLocY = h-200

    offset = h-180
    resetVis = -1

    try:
        with open(pi + "save.txt", "r") as save:
            saveList = save.readlines()
            if saveList == '':
                raise FileNotFoundError
            for i in range(len(saveList)): # Only operate after first line
                line = saveList[i]
                if i == 0: # For the first line
                    tickNum = int(line[findnth(line,'\t', 4):findnth(line,'\t', 5)])
                    secNum = int(line[findnth(line,'\t', 5):line.index('\n')])
                else: 
                    daySeries += [int(line[0:line.index('\t')])]
                    cSeries += [int(line[findnth(line,'\t', 0):findnth(line,'\t', 1)])]
                    tSeries += [int(line[findnth(line,'\t', 1):findnth(line,'\t', 2)])]
                    eSeries += [int(line[findnth(line,'\t', 2):findnth(line,'\t', 3)])]
                    bSeries += [int(line[findnth(line,'\t', 3):line.index('\n')])]
                    dayNum = daySeries[-1]
                    
                    
                    
            print ('Successfully read save')
    except FileNotFoundError:
            print ('No save found')
            daySeries = [0]
            cSeries = [0] # Callafiato is Orange
            tSeries = [0] # Teovedar is Purple
            eSeries = [0] # Ellazaire is Yellow
            bSeries = [0] # Baladeo is Blue
            dayNum = 0

    

    BEGINPLAY = USEREVENT+1
    beginPlay = pygame.event.Event(BEGINPLAY)
    pygame.event.post(beginPlay)

    while True: # the main game loop

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                if event.key == K_NUMLOCK:
                    addTo(5, cSeries) # Numlock only thinks its pressed when it is turned on
                    print ("Adding 5 to Callafiato") # so I have to have it trigger on up and down
            elif event.type == KEYDOWN:
                # Handle key presses
                if event.key == K_NUMLOCK:
                    addTo(5, cSeries)
                    print ("Adding 5 to Callafiato")
                elif event.key == K_KP_DIVIDE:
                    addTo(5, tSeries)
                    print ("Adding 5 to Teovedar")
                elif event.key == K_KP_MULTIPLY:
                    addTo(5, eSeries)
                    print ("Adding 5 to Ellazaire")
                elif event.key == K_BACKSPACE:
                    addTo(5, bSeries)
                    print ("Adding 5 to Baladeo")
                elif event.key == K_KP7:
                    addTo(1, cSeries)
                    print ("Adding 1 to Callafiato")
                elif event.key == K_KP8:
                    addTo(1, tSeries)
                    print ("Adding 1 to Teovedar")
                elif event.key == K_KP9:
                    addTo(1, eSeries)
                    print ("Adding 1 to Ellazaire")
                elif event.key == K_KP_MINUS:
                    addTo(1, bSeries)
                    print ("Adding 1 to Baladeo")
                elif event.key == K_KP4:
                    addTo(-1, cSeries)
                    print ("Subtracting 1 to Callafiato")
                elif event.key == K_KP5:
                    addTo(-1, tSeries)
                    print ("Subtracting 1 to Teovedar")
                elif event.key == K_KP6:
                    addTo(-1, eSeries)
                    print ("Subtracting 1 to Ellazaire")
                elif event.key == K_KP_PLUS:
                    addTo(-1, bSeries)
                    print ("Subtracting 1 to Baladeo")
                elif event.key == K_KP1:
                    addTo(-5, cSeries)
                    print ("Subtracting 5 to Callafiato")
                elif event.key == K_KP2:
                    addTo(-5, tSeries)
                    print ("Subtracting 5 to Teovedar")
                elif event.key == K_KP3:
                    addTo(-5, eSeries)
                    print ("Subtracting 5 to Ellazaire")
                elif event.key == K_KP_ENTER:
                    addTo(-5, bSeries)
                    print ("Subtracting 5 to Baladeo")

                elif event.key == K_KP0:
                    if reset == 1:
                        tickNum = 0
                        secNum = 0
                        dayNum = 0
                        daySeries = [0]
                        cSeries = [0]
                        tSeries = [0]
                        eSeries = [0]
                        bSeries = [0]
                        reset = 11
                        resetVis = -1
                    else:
                        reset -= 1
                        resetVis = 0
                    with open(pi + "save.txt", "w") as save:
                        saveString = "Time\tCallafiato\tTeovedar\tEllazaire\tBaladeo\t" + str(tickNum) + '\t' + str(secNum) + '\n'
                        for i in range(len(daySeries)):
                            saveString += str(daySeries[i]) + '\t' + str(cSeries[i]) + '\t' + str(tSeries[i]) + '\t' + str(eSeries[i]) + '\t' + str(bSeries[i]) + '\n'
                        save.write(saveString)

                elif event.key == K_KP_PERIOD:
                    if pi == '':
                        print ('Can\'t export saves, not on pi')
                    else:
                        dir = ''
                        output = subprocess.Popen("lsblk", stdout=subprocess.PIPE, shell=True)
                        for out in output.communicate()[0].split():
                            if '/media/' in str (out):
                                dir = out.decode('utf-8')
                                print (dir)
                                try:
                                    with open(dir + '/save.txt', "w") as save:
                                        saveString = "Time\tCallafiato\tTeovedar\tEllazaire\tBaladeo\n"
                                        for i in range(len(daySeries)):
                                            saveString += str(daySeries[i]) + '\t' + str(cSeries[i]) + '\t' + str(tSeries[i]) + '\t' + str(eSeries[i]) + '\t' + str(bSeries[i]) + '\n'
                                            save.write(saveString)
                                    os.system('sudo udisks --unmount /dev/sda')
                                    os.system('sudo udisks --detach /dev/sda')
                                except:
                                    print ("No save transferred")
                                            
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_x:
                    DISPLAYSURF = pygame.display.set_mode((w, h), pygame.RESIZABLE)
                elif event.key == K_f:
                    DISPLAYSURF = pygame.display.set_mode((w, h), pygame.FULLSCREEN)
                elif event.key == K_d:
                    secNum += 86400
                    
                #print(str(daySeries) + str(cSeries) + str(tSeries) + str(eSeries) + str(bSeries))

            DISPLAYSURF.blit(backImg, backImg.get_rect())
            
            fit = -min(6, (offset-110)/max(cSeries[-1], tSeries[-1], eSeries[-1], bSeries[-1],1))

            cLocY = min(cSeries[-1] * fit + offset,offset)
            tLocY = min(tSeries[-1] * fit + offset,offset)
            eLocY = min(eSeries[-1] * fit + offset,offset)
            bLocY = min(bSeries[-1] * fit + offset,offset)

            DISPLAYSURF.blit(cImg, (cLocX, cLocY))
            DISPLAYSURF.blit(tImg, (tLocX, tLocY))
            DISPLAYSURF.blit(eImg, (eLocX, eLocY))
            DISPLAYSURF.blit(bImg, (bLocX, bLocY))

            DISPLAYSURF.blit(baseImg, (w/2-600, h-100))
            
            ShadeSetX = 7
            ShadeSetY = 6

            cShadeSurf = BASICFONT.render(str(cSeries[-1]), 1, (187, 80, 39))
            cShadeRect = cShadeSurf.get_rect()
            cShadeRect.center = (cLocX+140+ShadeSetX, min(cLocY+100+ShadeSetY,h-100+ShadeSetY))
            DISPLAYSURF.blit(cShadeSurf, cShadeRect)

            tShadeSurf = BASICFONT.render(str(tSeries[-1]), 1, (104, 41, 125))
            tShadeRect = tShadeSurf.get_rect()
            tShadeRect.center = (tLocX+140+ShadeSetX, min(tLocY+100+ShadeSetY,h-100+ShadeSetY))
            DISPLAYSURF.blit(tShadeSurf, tShadeRect)

            eShadeSurf = BASICFONT.render(str(eSeries[-1]), 1, (199, 169, 47))
            eShadeRect = eShadeSurf.get_rect()
            eShadeRect.center = (eLocX+140+ShadeSetX, min(eLocY+100+ShadeSetY,h-100+ShadeSetY))
            DISPLAYSURF.blit(eShadeSurf, eShadeRect)

            bShadeSurf = BASICFONT.render(str(bSeries[-1]), 1, (38, 55, 125))
            bShadeRect = bShadeSurf.get_rect()
            bShadeRect.center = (bLocX+140+ShadeSetX, min(bLocY+100+ShadeSetY,h-100+ShadeSetY))
            DISPLAYSURF.blit(bShadeSurf, bShadeRect)
            
            cScoreSurf = BASICFONT.render(str(cSeries[-1]), 1, (255, 255, 255))
            cScoreRect = cScoreSurf.get_rect()
            cScoreRect.center = (cLocX+140, min(cLocY+100,h-100))
            DISPLAYSURF.blit(cScoreSurf, cScoreRect)

            tScoreSurf = BASICFONT.render(str(tSeries[-1]), 1, (255, 255, 255))
            tScoreRect = tScoreSurf.get_rect()
            tScoreRect.center = (tLocX+140, min(tLocY+100,h-100))
            DISPLAYSURF.blit(tScoreSurf, tScoreRect)

            eScoreSurf = BASICFONT.render(str(eSeries[-1]), 1, (255, 255, 255))
            eScoreRect = eScoreSurf.get_rect()
            eScoreRect.center = (eLocX+140, min(eLocY+100,h-100))
            DISPLAYSURF.blit(eScoreSurf, eScoreRect)

            bScoreSurf = BASICFONT.render(str(bSeries[-1]), 1, (255, 255, 255))
            bScoreRect = bScoreSurf.get_rect()
            bScoreRect.center = (bLocX+140, min(bLocY+100,h-100))
            DISPLAYSURF.blit(bScoreSurf, bScoreRect)
            
            daySurf = SMALLFONT.render(str(dayNum), 1, (127, 0, 45))
            dayRect = daySurf.get_rect()
            dayRect.center = (w-10, 10)
            DISPLAYSURF.blit(daySurf, dayRect)
            
            if resetVis >= 0:
                resetSurf = BASICFONT.render("Reset all scores in " + str(reset), 1, (44, 39, 53))
                resetRect = resetSurf.get_rect()
                resetRect.center = (w/2, h/2)
                DISPLAYSURF.blit(resetSurf, resetRect)
            if saveGame == True:
                saveGame = False
                # then saveGame as a file that can easily be pasted into a spreadsheet
                with open(pi + "save.txt", "w") as save:
                    saveString = "Time\tCallafiato\tTeovedar\tEllazaire\tBaladeo\t" + str(tickNum) + '\t' + str(secNum) + '\n'
                    for i in range(len(daySeries)):
                        saveString += str(daySeries[i]) + '\t' + str(cSeries[i]) + '\t' + str(tSeries[i]) + '\t' + str(eSeries[i]) + '\t' + str(bSeries[i]) + '\n'
                    save.write(saveString)
                    print ('Saved')
            if pi == '':
                print ('Can\'t export saves, not on pi')
            else:
                dir = ''
                output = subprocess.Popen("lsblk", stdout=subprocess.PIPE, shell=True)
                for out in output.communicate()[0].split():
                    if '/media/' in str (out):
                        dir = out.decode('utf-8')
                        print (dir)
                        try:
                            with open(dir + '/save.txt', "w") as save:
                                saveString = "Time\tCallafiato\tTeovedar\tEllazaire\tBaladeo\t" + str(tickNum) + '\t' + str(secNum) + '\n'
                                for i in range(len(daySeries)):
                                    saveString += str(daySeries[i]) + '\t' + str(cSeries[i]) + '\t' + str(tSeries[i]) + '\t' + str(eSeries[i]) + '\t' + str(bSeries[i]) + '\n'
                                save.write(saveString)
                            os.system('sudo udisks --unmount /dev/sda')
                            os.system('sudo udisks --detach /dev/sda')
                            print('ejected!')

                        except:
                            print ("No save transferred")

            pygame.display.update()
        
        # Calculate rough amount of time that has passed
        # so that save file for spreadsheets can have day
#        print('raw')
#        print(fpsClock.get_rawtime())
#        print('time')
#        print(fpsClock.get_time())
        tickNum += fpsClock.get_time()
        
        
        
        if tickNum >= 1000:
            tickNum -= 1000
            secNum += 1
            if resetVis >= 0:
                resetVis += 1
                if resetVis >= 2:
                    resetVis = -1
                    pygame.event.post(beginPlay)
        if secNum >= 86400:
            secNum -= 86400
            dayNum += 1
            reset = 11
            print ("Days: " + str(dayNum))
#        print("Sec: " + str(secNum) + " Tick: " + str(tickNum))
        fpsClock.tick(FPS)
        
def addTo(added, team):
    global daySeries, cSeries, tSeries, eSeries, bSeries, pi, saveGame
    
    # if datapoint is on a different day, add a new point.
    if daySeries[-1] != dayNum:
        daySeries += [dayNum]
        cSeries += [cSeries[-1]]
        tSeries += [tSeries[-1]]
        eSeries += [eSeries[-1]]
        bSeries += [bSeries[-1]]
        # after there is a new point, then update the score
    team[-1] = team[-1]+added
    saveGame = True # Save after updating picture to reduce visual lag

def findnth(haystack, needle, n):
    parts= haystack.split(needle, n+1)
    if len(parts)<=n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)

if __name__ == '__main__':
    main()
