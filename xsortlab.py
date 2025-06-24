from cmu_graphics import *
import random

'''
Video link:
https://1drv.ms/v/c/25b10959adea1081/Ee-sqDbxi6lNsbeONhu60-kByrBgr0jywyARBdB6YoZQcA?e=dPWr09

This is one of the project 1 options which replicates a sorting simulator. xSortLab allows
one to pick a sort size, and run the app such that bars of various heights are sorted in increasing
order. The app showcases a temporary location where bars are 'swapped' as well as displays 
those bars that have been sorted thus far in black as opposed to grey. The bars being compared
are outlined in green boxes and the current max value (not already sorted and black) will be labeled
as 'max.' 

Some features include, automatic step, manual step, pausing, fast mode, randomizing a new sort, and being able to 
input a new size. When selecting these options (buttons), the buttons become a darker color which indicates
that they were pressed. 

It should also be noted that the number of comparisons and copies are recorded for each sort. After each comparison,
one is added to the comparison count. Each time the 'temporary' space is used and bars are sorted / switched,
the amount of copies is updated by one and the count is displayed under the comparison count.

The class that I implemented was the Sort Class, which takes in a size of how many 'bars' need to be sorted,
as well as the max height of all the bars. These parameters allow for a list to be made with decreasing heights.
This list is then shuffled so that the order is random. In addition, the class includes a method which sorts bars each 
time we reach the end of the list. Once we have made all comparisons, the sort method is called which swaps the bar with 
the current maximum height with that of the other current bar that is highlighted. This ensures that the end product
will display a sorted arrangement of black bars.

'''

class Sort:
    def __init__(self, size, maxHeight):
        self.foundList = []
        self.width = 560 // size // 1.5
        self.sortList = []
        for i in range(size):
            self.sortList.append(maxHeight - (maxHeight // size)*i)
        random.shuffle(self.sortList)
        self.temp = None
    
    def sort(self, maxIndex):
        self.foundList = [self.sortList[maxIndex]] + self.foundList
        if self.sortList[maxIndex] != self.sortList[-1]:
            self.sortList = self.sortList[:maxIndex] + [self.sortList[-1]] + self.sortList[maxIndex + 1:-1]
        else:
            self.sortList = self.sortList[:maxIndex]
    
        
def onAppStart(app):
    app.width = 800
    app.height = 600
    app.size = 16
    newGame(app)

def newGame(app):
    app.comparisons = 0
    app.copies = 0
    app.maxIndex = 0
    app.currIndex = 1
    app.maxHeight = 133
    app.paused = False
    app.stepsPerSecond = 5
    app.prevMaxIndex = None
    app.sort = Sort(app.size, app.maxHeight)
    app.lengthOfBars = len(app.sort.sortList)
    app.run = False
    app.pressedIndex = None
    app.chooseNewSize = False
    app.newSize = ''

def redrawAll(app):
    drawRect(80, 100, 560, 400, fill = 'snow', border = 'darkOliveGreen')
    drawLabel('Visual Selection Sort', 154, 80, size=16)
    drawLabel('Temp', 360, 484, bold = True)
    drawLabel(f'Comparisons {app.comparisons}', 735, 560)
    drawLabel(f'Copies {app.copies}', 751, 580)
    for i in range(len(app.sort.sortList)):
        bottomBarY = 300
        bottomBarX = 80 + app.sort.width // 2.5 + (app.sort.width + app.sort.width // 2)*i
        if i != app.sort.temp:
            drawRect(bottomBarX, bottomBarY, app.sort.width, app.sort.sortList[i], 
                    fill = 'lightSteelBlue', border = 'black', align = 'left-bottom')
        if (app.currIndex == i or (app.maxIndex == i and app.currIndex > 0) or (app.prevMaxIndex == i and app.currIndex < 0)):
            drawRect(bottomBarX, bottomBarY + 5, app.sort.width, 200, 
                    fill = None, border = 'seaGreen', align = 'left-bottom')
            if i == app.maxIndex or i == app.prevMaxIndex:
                cx = bottomBarX + app.sort.width / 2
                cy = 315
                drawLabel('max', cx, cy, size = 10)
        if app.sort.temp == i:
            #drawing temp bar at the bottom (slightly bigger width)
            drawRect(343, 457, app.sort.width * 1.5, app.sort.foundList[0],
                    fill = 'lightSteelBlue', border = 'black', align = 'left-bottom')
            # need to still draw bar at the end that is being moved even though it is being rearranged
            lastIndex = len(app.sort.sortList) 
            barX = 80 + app.sort.width // 2.5 + (app.sort.width + app.sort.width // 2)*lastIndex
            barY = 300
            drawRect(barX, barY, app.sort.width, app.sort.sortList[i],
                    fill = 'lightSteelBlue', border = 'black', align = 'left-bottom')
    for i in range(len(app.sort.foundList)):
        bottomBarY = 300
        lastIndex = len(app.sort.sortList)
        bottomBarX = 80 + app.sort.width // 2.5 + (app.sort.width + app.sort.width // 2)*(lastIndex+i)
        if app.sort.temp == None or (len(app.sort.foundList) > 1 and i > 0) or len(app.sort.foundList) == app.size:
            drawRect(bottomBarX, bottomBarY, app.sort.width, app.sort.foundList[i], 
                    fill = 'black', align = 'left-bottom')
    
    if app.chooseNewSize:
        drawLabel(f'New Size: {app.newSize}', 725, 503)
        drawLabel('Please enter numbers to input the new size; then click enter to enact the change (maximum size is 32)',
                    505, 523)
    
    for i in range(6):
        topY = 100 + 67*i
        topX = 696
        buttons = ['New Sort', 'Run', 'Pause', 'Step', 'Fast Mode', 'New Size']
        if (i == 2 and not app.paused) or (i == 4 and app.stepsPerSecond == 5):
            color = 'lightGray'
        elif (i == app.pressedIndex) or (i == 2 and app.paused): 
            color = 'grey'
        else: 
            color = 'lightGray'
        drawRect(topX, topY, 80, 50, fill = color)
        drawLabel(buttons[i], topX + 40, topY + 25)
            
def onStep(app):
    if not app.paused and app.run:
        takeStep(app)

def onMousePress(app, mouseX, mouseY):
    app.chooseNewSize = False
    buttonIndex = getButton(app, mouseX, mouseY)
    app.pressedIndex = buttonIndex
    if buttonIndex == 0:
        newGame(app)
    if buttonIndex == 1:
        app.run = True
    if buttonIndex == 2:
        app.paused = not app.paused
    if buttonIndex == 3:
        takeStep(app)
    if buttonIndex == 4:
        if app.stepsPerSecond == 5:
            app.stepsPerSecond = 10
        else:
            app.stepsPerSecond = 5
    if buttonIndex == 5:
        app.chooseNewSize = True
    
def getButton(app, mouseX, mouseY):
    if 696 <= mouseX <= 776:
        if 100 <= mouseY <= 150: return 0
        elif 167 <= mouseY <= 217: return 1
        elif 233 <= mouseY <= 283: return 2
        elif 300 <= mouseY <= 350: return 3
        elif 367 <= mouseY <= 417: return 4
        elif 433 <= mouseY <= 483: return 5

def takeStep(app):
    if len(app.sort.sortList) == 0:
        return
    if app.currIndex < len(app.sort.sortList) - 1:
        app.sort.temp = None
        if app.sort.sortList[app.currIndex] > app.sort.sortList[app.maxIndex] and app.currIndex > 0:
            app.maxIndex = app.currIndex
        app.comparisons += 1
        app.currIndex += 1
        
    elif app.currIndex == len(app.sort.sortList) - 1:
        if app.sort.sortList[app.currIndex] > app.sort.sortList[app.maxIndex]:
            app.maxIndex = app.currIndex
        app.prevMaxIndex = app.maxIndex
        app.sort.temp = app.maxIndex
        app.copies += 1
        app.sort.sort(app.maxIndex)
        app.currIndex = -1
        app.maxIndex = 0

def onKeyPress(app, key):
    if app.chooseNewSize:
        if key.isdigit():
            app.newSize += key
    if key == 'backspace':
        app.newSize = app.newSize[:-1]
    if key == 'enter':
        if 0 < int(app.newSize) < 33:
            app.size = int(app.newSize)
            newGame(app)
        app.newSize = ''

def main():
    runApp()
main()
    
