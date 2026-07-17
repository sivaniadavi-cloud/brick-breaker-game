
from cmu_graphics import *
import random

class Ball:
    def __init__(self, cx, cy, dx, dy, r):
        self.cx = cx
        self.cy = cy
        self.dx = dx
        self.dy = dy
        self.r = 10
        
    def move(self, app):
        self.cx += self.dx
        self.cy += self.dy
        
        if self.cx + self.r >= app.width:
            self.cx = app.width - self.r
            self.dx = -self.dx
            
        elif self.cx - self.r <= 0:
            self.cx = self.r
            self.dx = -self.dx
        
        if self.cy - self.r <= 0:
            self.cy = self.r
            self.dy = -self.dy
            
        if self.wallCollisions(app):
            self.dy = -self.dy
            if app.counter % 5 == 0 and app.counter != 0:
                app.stepsPerSecond += 10
                if len(app.balls) < 5:
                    app.balls.append(Ball(app.width//2, app.height//2, 5, 5, 20))
        
    def wallCollisions(self, app):
        inXBound = ((app.rectX <= self.cx + self.r <= app.rectX + app.rectWidth) 
                or (app.rectX <= self.cx - self.r <= app.rectX + app.rectWidth))
        inYBound = (self.cy + self.r == app.rectY)
        return inXBound and inYBound
    
    def brickCollision(self, app):
        for row in range(app.rows):
            for col in range(app.cols):
                brick = app.board[row][col]
                if not brick.isBroken:
                    if ((brick.left <= self.cx <= (brick.left + brick.width)) and 
                        (brick.top <= self.cy <= (brick.top + brick.height))):
                        brick.takeHit(app)
                        self.dy = -self.dy
                        return
    
    def draw(self):
        drawCircle(self.cx, self.cy, self.r, fill='purple')
        
class Brick:
    def __init__(self, left, top, width, height, color):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.color = color
        self.isBroken = False
        
    def takeHit(self, app):
        if not self.isBroken:
            self.isBroken = True
            app.bricksRemaining -= 1
            app.counter += 1
        
            if random.random() < 0.2:
                powerType = random.choice(['Wide', 'Life'])
                app.powerUps.append(PowerUp(self.left + self.width//2,
                                            self.top + self.height/2, powerType))
    
            spawnParticles(app, self.left+self.width/2, self.top+self.height/2, self.color)
        
    def draw(self):
        if not self.isBroken:
            drawRect(self.left, self.top, self.width, self.height, fill=self.color)
            
class StrongBrick(Brick):
    def __init__(self, left, top, width, height, color):
        super().__init__(left, top, width, height, color)
        self.hitsLeft = 3
    
    def takeHit(self, app):
        if not self.isBroken:
            self.hitsLeft -= 1
            if self.hitsLeft == 2:
                self.color = 'royalBlue'
            elif self.hitsLeft == 1:
                self.color = 'lightBlue'
    
            if self.hitsLeft <= 0:
                self.isBroken = True
                app.bricksRemaining -= 1
                app.counter += 5
                spawnParticles(app, self.left+self.width/2, self.top+self.height/2, 'white')
            
    def draw(self):
        if not self.isBroken:
            super().draw()
            drawLabel(self.hitsLeft, self.left + self.width/2, 
                      self.top + self.height/2, fill='white', bold=True)

class PowerUp:
    def __init__(self, cx, cy, type):
        self.cx = cx
        self.cy = cy
        self.r = 12
        self.type = type
        self.color = 'yellow' if type == 'Wide' else 'green'
        self.dy = 3
        
    def move(self):
        self.cy += self.dy
    
    def draw(self):
        drawCircle(self.cx, self.cy, self.r, fill=self.color, border='black')
        drawLabel(self.type[0], self.cx, self.cy, bold=True)

class Particle:
    def __init__(self, cx, cy, color):
        self.cx = cx
        self.cy = cy
        self.color = color
        self.dx, self.dy = random.uniform(-4, 4), random.uniform(-4, 4)
        self.life = 20
        
    def move(self):
        self.cx += self.dx
        self.cy += self.dy
        self.life -= 1
    
    def draw(self):
        drawRect(self.cx, self.cy, 4, 4, fill=self.color, opacity=self.life*5)

# Button class adapted from lecture
class Button:
    def __init__(self, left, top, width, height, color, text, onClickFn):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.onClickFn = onClickFn
        
    def handleClick(self, mouseX, mouseY):
        left, right = self.left, self.left + self.width
        top, bottom = self.top, self.top + self.height
        if (left <= mouseX <= right) and (top <= mouseY <= bottom):
            self.onClickFn()
            
    def draw(self):
        drawRect(self.left, self.top, self.width, self.height, fill=self.color)
        cx, cy = self.left + self.width/2, self.top + self.height/2
        drawLabel(self.text, cx, cy, size=14)

def onAppStart(app):
    app.rectWidth = 50
    app.rectHeight = 20
    app.scores = {0}
    
    app.rows = 5
    app.cols = 5
    app.boardLeft = 0
    app.boardTop = 0
    app.boardWidth = app.width
    app.boardHeight = 0.25 * app.height
    app.cellBorderWidth = 2
    app.board = [([None] * app.cols) for row in range(app.rows)]
    app.instructcy = app.width*.25
    app.tooManyBalls = False
    
    app.lives = 3
    resetApp(app)
    initializeButtons(app)
    
def gameOverReset(app):
    app.lives = 3
    
def resetApp(app):
    gameOverReset(app)
    app.balls = [ Ball(app.width//2, app.height//2, 5, 5, 20) ]
    app.rectX = app.width//2 - app.rectWidth//2
    app.rectY = app.height * 0.875
    app.counter = 0
    app.gameOver = False
    app.paused = True
    app.win = False
    app.stepsPerSecond = 30
    app.bricksRemaining = app.rows*app.cols
    app.powerUps = []
    app.particles = []
    createBrickBoard(app)

def start_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='yellow', opacity=20)
    drawLabel('Press space to see instructions!', 200, 240, size=16)
    title = 'Play Brick Breaker'
    spacing = 16
    totalTextWidth = len(title) * spacing
    startX = app.width/2 - totalTextWidth/2 + spacing/2
    for i in range(len(title)):
        color = 'red' if i % 2 == 0 else 'blue'
        drawLabel(title[i], startX + i*spacing, app.height*0.4, size=26, fill=color, bold=True)

def start_onKeyPress(app, key):
    if key == 'space':
        setActiveScreen('instruct')
        
def instruct_onScreenActivate(app):
    app.instructcy = app.height*0.25

def instruct_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='lightGreen', opacity=40)
    for button in app.buttons:
        button.draw()
    instructions = ['Press space to start the game!',
                    'Break as many bricks as you can.', 
                    'As you break more bricks,', 
                    'the balls will speed up and', 
                    'more balls will be added.',
                    'Press the ? at the bottom left to see',
                    'the instructions again.',
                    ]
    for i in range(len(instructions)):
        fill = 'red' if instructions[i] == instructions[-1] or instructions[i] == instructions[-2] else 'black'
        cy = app.instructcy + (i*20)
        drawLabel(instructions[i], app.width//2, cy, size=12, bold=True, fill=fill)
        
def instruct_onMousePress(app, mouseX, mouseY):
    for button in app.buttons:
        button.handleClick(mouseX, mouseY)

def instruct_onStep(app):
    if app.instructcy < app.height*.7:
        app.instructcy += 0.1
    else:
        app.instructcy = app.height * .25

def instruct_onKeyPress(app, key):
    if key == 'space':
        setActiveScreen('game')
        
def powers_redrawAll(app):
    drawLabel('Power Ups will fall as you break some bricks.', app.width//2, app.height*.25, size=20)
    drawLabel('W: Wide Paddle. The paddle will grow horizontally.', app.width//2, app.height*.33, size=15)
    drawLabel('L: Extra Life. You will gain an extra life.', app.width//2, app.height*0.4, size=15)
    app.backButton.draw()

def powers_onMousePress(app, mouseX, mouseY):
    app.backButton.handleClick(mouseX, mouseY)
    
def keys_redrawAll(app):
    instructions = ["Hold 'tab' to speed up and down arrow to slow down",
                    "Hold right and left arrows to move the paddle.",
                    "You can pause and unpause",
                    "the game by pressing 'p'",
                    "You can add balls by pressing 'b'",
                    'You can only have a maximum of', 
                    '5 balls at a time.']
    
    for i in range(len(instructions)):
        drawLabel(instructions[i], app.width//2, 150 + (i*30), size=12, bold=True)
        app.backButton.draw()
        
def keys_onMousePress(app, mouseX, mouseY):
    app.backButton.handleClick(mouseX, mouseY)

def points_redrawAll(app):
    instructions = ['You gain one point for every brick',
                    'broken and lose a point', 
                    'for every ball that hits the ground.',
                    'For strong bricks, (bricks that take multiple hits)',
                    'breaking those is worth 5 points.']
    for i in range(len(instructions)):
        cy = app.instructcy + (i*20)
        drawLabel(instructions[i], app.width//2, cy, size=12, bold=True)
    app.backButton.draw()
    
def points_onMousePress(app, mouseX, mouseY):
    app.backButton.handleClick(mouseX, mouseY)

def getBackgroundColor(app):
    colors = ['yellow', 'orange', 'pink', 'red']
    i = app.counter // 5
    if i >= len(colors):
        color = colors[-1]
    else:
        color = colors[i]
    return color

def game_redrawAll(app):
    drawRect(0, app.height-50, 50, 50, fill='cyan', border='black')
    drawLabel('?', 25, app.height-25, bold=True, size=30)
    
    if app.win:
        drawRect(0, 0, app.width, app.height, fill='lightBlue', opacity=40)
        drawLabel('You won!', app.width//2, app.height//2, bold=True, size=50, fill='green')
        drawLabel('Press r to restart the game', app.width//2, app.height*.75, size=20)
    
    elif not app.gameOver:
        color = getBackgroundColor(app)
        drawRect(0, 0, app.width, app.height, fill=color, opacity=50)
        drawBoard(app)
        drawLabel(app.counter, app.width//2, app.height//2, size=100, opacity=60, font='montserrat', bold=True)
        drawRect(app.rectX, app.rectY, app.rectWidth, app.rectHeight)
        drawLabel(f'High Score: {max(app.scores)}', app.width//2, app.height*0.75//2, size=15)
        if app.tooManyBalls:
            drawLabel('You have reached max balls!', app.width//2, app.height*0.4, fill='red', size=13)
        
        for ball in app.balls:
            ball.draw()
        
        for i in range(app.lives):
            drawCircle(30+(i*15), app.height-70, 5, fill='red')
        drawLabel(f'Lives: {app.lives}', 30, app.height-85, align='left')
        
        for particle in app.particles:
            particle.draw()
        
        for power in app.powerUps:
            power.draw()
        
    else:
        drawRect(0, 0, app.width, app.height, fill='black', opacity=50)
        drawLabel(f'Score: {app.counter}', app.width//2, app.height * 0.5//2, size=30, bold=True, fill='white', font='montserrat')
        drawLabel('GAME OVER', app.width//2, app.height//2, size=40, fill='red', font='montserrat', bold=True)
        drawLabel('Press r to reset', app.width//2, app.height * 0.75, size=20, fill='white', font='montserrat', bold=True)

def game_onScreenActivate(app):
    resetApp(app)

def game_onMousePress(app, mouseX, mouseY):
    if (pointInRect(0, app.height-50, 50, 50, mouseX, mouseY)):
        setActiveScreen('instruct')

def game_onKeyPress(app, key):
    if key == 'p':
        app.paused = not app.paused
    if key == 's':
        app.win = True 
    if key == 'r':
        resetApp(app)
    if key == 'b' and len(app.balls) < 5:
        app.balls.append(Ball(app.width//2, app.height//2, 5, 5, 20))
        app.tooManyBalls = False
    elif key == 'b':
        app.tooManyBalls = True

def game_onKeyHold(app, keys):
    if 'right' in keys:
        app.rectX += 5
    if 'left' in keys:
        app.rectX -= 5
    if app.rectX + app.rectWidth > app.width:
        app.rectX = app.width - app.rectWidth
    if app.rectX < 0:
        app.rectX = 0
    if 'tab' in keys:
        app.stepsPerSecond = 100
    elif 'down' in keys:
        app.stepsPerSecond = 15
    else:
        app.stepsPerSecond = 30

def game_onStep(app):
    if not app.paused and not app.gameOver:
        # move the balls
        for ball in list(app.balls):
            ball.move(app)
            ball.brickCollision(app)
            if ball.cy + ball.r >= app.height:
                app.balls.remove(ball)
                app.counter -= 1
                app.tooManyBalls = False
        # losing lives logic
        if len(app.balls) == 0:
            app.lives -= 1
            if app.lives > 0:
                app.balls.append(Ball(app.width//2, app.height//2, 5, -5, 10))
                app.paused = True
                app.tooManyBalls = False
            else:
                app.gameOver = True
                app.paused = True
                if app.counter < 0:
                    app.counter = 0
                app.scores.add(app.counter)
        # power up catching
        for p in list(app.powerUps):
            p.move()
            if ((app.rectX <= p.cx <= app.rectX + app.rectWidth) and
                app.rectY <= p.cy + p.r <= app.rectY + app.rectHeight):
                
                if p.type == 'Wide':
                    app.rectWidth += 20
                elif p.type == 'Life':
                    app.lives += 1
                app.powerUps.remove(p)
            elif p.cy > app.height:
                app.powerUps.remove(p)
        # update particles
        for part in list(app.particles):
            part.move()
            if part.life <= 0: 
                app.particles.remove(part)
    # game over logic
    if app.bricksRemaining == 0:
        app.win = True
        app.paused = True
                    
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            brick = app.board[row][col]
            brick.draw()

def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)
    
def pointInRect(left, top, width, height, mouseX, mouseY):
    return ((left <= mouseX <= (left + width)) and (top <= mouseY <= (top + height)))

def createBrickBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            left, top = getCellLeftTop(app, row, col)
            width, height = getCellSize(app)
            randNum = random.random()
            if randNum < 0.3:
                app.board[row][col] = StrongBrick(left, top, width, height, 'blue')
            else:
                if (col % 2 == 0 and row % 2 == 0) or (col % 2 == 1 and row % 2 == 1):
                    color = 'pink'
                else:
                    color = 'blue'
                app.board[row][col] = Brick(left, top, width, height, color)
            
def spawnParticles(app, x, y, color):
    for _ in range(10):
        app.particles.append(Particle(x, y, color))
        
def initializeButtons(app):
    def powersButtonOnClick():
        setActiveScreen('powers')
    def keysButtonOnClick():
        setActiveScreen('keys')
    def pointsButtonOnClick():
        setActiveScreen('points')
    def backClick():
        setActiveScreen('instruct')
    
    powers = Button(20, 20, 100, 40, 'yellow', 'Power-Ups', powersButtonOnClick)
    keys = Button(140, 20, 100, 40, 'orange', 'Key Shortcuts', keysButtonOnClick)
    points = Button(260, 20, 100, 40, 'blue', 'Scoring', pointsButtonOnClick)
    app.buttons = [powers, keys, points]
    
    app.backButton = Button(20, 340, 80, 40, 'gray', 'BACK', backClick)
    
def main():
    runAppWithScreens(initialScreen='start')

main()
