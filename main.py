from cmu_graphics import *
import random
import time
import hashlib
import os
import ast

app.background = rgb(142,121,102)
app.isShowingInstructions = True
app.inMainMenu = False
app.inClassicGame = False
app.inSpeedRunGame = False
app.editingUsername = False
app.justExitedEditingMode = False
app.isSigningIn = False
app.isEditingSignUpUsername = False
app.isEditingSignUpPassword = False
app.isLoggedIn = False
app.submittedCredentials = False
app.justExitedSignUpEditingMode = False
app.isShowingLoginResult = False
app.isShowingUsernameChangeResult = False
app.isShowingLeaderboard = False
app.inSpeedRunGame = False
app.hasStartedSpeedRunning = False
app.gridIsFull = False
app.speedRunStartTime = None
app.currentlyCheckingFor = 16
app.newTime = []
app.speedRunLeaderboard = None
app.isShowingSpeedRunLeaderboard = False
app.leaderboard = None
app.currentPage = 0
app.currentLabels = Group()

pages = [
    [
        "2048 Game Instructions",
        "",
        "1. Getting Started",
        "  - Login/Sign Up to Play:",
        "    Create a new account or log in with your existing",
        "    credentials to start playing the game."
    ],
    [
        "2. How to Play - Classic Mode",
        "  - Objective:",
        "    Merge tiles with the same numbers to create tiles",
        "    with higher numbers, aiming to form a tile with the",
        "    number 2048.",
        "",
        "  - Controls:",
        "    Use the WASD keys or Arrow Keys to move the tiles on",
        "    the board:",
        "    - W or Up Arrow: Move tiles up.",
        "    - A or Left Arrow: Move tiles left.",
        "    - S or Down Arrow: Move tiles down.",
        "    - D or Right Arrow: Move tiles right.",
        "    When two tiles with the same number collide, they",
        "    merge into a new tile with their combined value."
    ],
    [
        "  - Gameplay:",
        "    Start with a grid containing a few numbered tiles.",
        "    Each move adds a new tile to the grid.",
        "    Slide the tiles in any direction to combine tiles of",
        "    the same number.",
        "    The game continues until you create a tile with the",
        "    number 2048 or you can no longer make moves.",
        "",
        "  - Winning and Beyond:",
        "    Achieve a 2048 tile to win the game.",
        "    You can choose to continue playing to reach higher",
        "    scores and larger numbered tiles."
    ],
    [
        "2. How to Play - Speed Run Mode",
        "  - Objective:",
        "    Merge tiles as quickly as possible, aiming to create",
        "    the highest numbered tile in the shortest amount of",
        "    time.",
        "  - How It Works:",
        "    Your time starts being tracked once you create a tile",
        "    with the number 16.",
        "    Continue combining tiles to create higher-numbered",
        "    tiles, with your time recorded from the moment the",
        "    16 tile appears. The goal is to reach the highest",
        "    possible tile number in the shortest time.",
        "  - Scoring:",
        "    Your performance in Speed Run mode is evaluated based",
        "    on how fast you can combine tiles to create larger",
        "    numbers. Track your best times and strive to beat them",
        "    in subsequent games."
    ],
    [
        "3. Additional Controls",
        "  - 'i' Key:",
        "    Press the 'i' key to bring up these instructions",
        "    again when in the main menu",
        "",
        "  - 'Escape' Key:",
        "    Press the 'escape' key to go back to the main menu",
        "    or previous screen."
    ]
]

def drawPage():
    app.currentLabels.clear()
    app.currentLabels.add(
        Rect(15, 15, 370, 370, fill = rgb(250, 248, 239)),
        createSmoothCorners(370, 200, 200, rgb(142, 121, 102), rgb(250, 248, 239)),
        Rect(15, 15, 370, 370, fill = rgb(250, 248, 239)),
        createSmoothCorners(370, 200, 200, rgb(142, 121, 102), rgb(250, 248, 239)),
        Rect(15, 15, 370, 50, fill = rgb(236, 231, 220)),
        createUICornerRect(370, 200, 200, rgb(142, 121, 102)),
        createUICornerCircles(370, 200, 200, rgb(236, 231, 220)),
        Label('Instructions', 200, 40, fill = rgb(142, 121, 102), font = 'arial', bold = True, size = 20, align = 'center')
    )
    x, y = 20, 80
    line_height = 18
    
    currentInstructions = pages[app.currentPage]
    
    for line in currentInstructions:
        label = Label(line, x + 3, y, fill=rgb(142, 121, 102), align='left', size=14, bold = True)
        app.currentLabels.add(label)
        y += line_height
    
    if app.currentPage > 0:
        prevLabel = Label("< Previous", 60, 40, fill=rgb(142, 121, 102), align='center', size=14, bold = True)
        app.currentLabels.add(prevLabel)
    if app.currentPage < len(pages) - 1:
        nextLabel = Label("Next >", 340, 40, fill=rgb(142, 121, 102), align='center', size=14, bold = True)
        app.currentLabels.add(nextLabel)



USER_DATA_FILE = 'users.txt'
HIGH_SCORES_FILE = 'high_scores.txt'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def read_users():
    if not os.path.exists(USER_DATA_FILE):
        return {}

    users = {}
    with open(USER_DATA_FILE, 'r') as file:
        for line in file:
            username, hashed_password = line.strip().split(':')
            users[username] = hashed_password
    return users

def write_users(users):
    with open(USER_DATA_FILE, 'w') as file:
        for username, hashed_password in users.items():
            file.write(f"{username}:{hashed_password}\n")

def read_high_scores():
    if not os.path.exists(HIGH_SCORES_FILE):
        return {}

    high_scores = {}
    with open(HIGH_SCORES_FILE, 'r') as file:
        for line in file:
            username, score = line.strip().split(':')
            high_scores[username] = int(score)
    return high_scores

def write_high_scores(high_scores):
    with open(HIGH_SCORES_FILE, 'w') as file:
        for username, score in high_scores.items():
            file.write(f"{username}:{score}\n")

def submit_high_score(username, score):
    high_scores = read_high_scores()

    if username in high_scores:
        if score > high_scores[username]:
            high_scores[username] = score
            result = 1
        else:
            result = 2
    else:
        high_scores[username] = score
        result = 3
    write_high_scores(high_scores)
    return result


def read_best_times():
    if not os.path.exists('best_times.txt'):
        return {}
    best_times = {}
    with open('best_times.txt', 'r') as file:
        for line in file:
            username, times = line.strip().split(';')
            best_times[username] = ast.literal_eval(times)
    return best_times

def convert_to_milliseconds(time_str):
    minutes, seconds_milliseconds = time_str.split(':')
    seconds, milliseconds = seconds_milliseconds.split('.')
    minutes = int(minutes)
    seconds = int(seconds)
    milliseconds = int(milliseconds)
    total_milliseconds = (minutes * 60 * 1000) + (seconds * 1000) + milliseconds
    return total_milliseconds

def write_best_times(best_times):
    with open('best_times.txt', 'w') as file:
        for username, times in best_times.items():
            file.write(f"{username};{times}\n")

def update_best_times(username, times):
    best_times = read_best_times()
    best_time = best_times[username]
    newTimes = []
    for i in range(12):
        if times[i] != '00:00.000':
            newTime = convert_to_milliseconds(times[i])
            oldTime = convert_to_milliseconds(best_time[i])
            if oldTime == 0:
                newTimes.append(times[i])
            elif newTime < oldTime:
                newTimes.append(times[i])
            else:
                newTimes.append(best_time[i])
        else:
            newTimes.append(best_time[i])
    best_times[username] = newTimes
    write_best_times(best_times)

def handle_authentication(username, password):
    users = read_users()
    if username in users:
        if users[username] == hash_password(password):
            return 1
        else:
            return 2
    else:
        users[username] = hash_password(password)
        write_users(users)
        high_scores = read_high_scores()
        high_scores[username] = 0
        write_high_scores(high_scores)
        best_times = read_best_times()
        best_times[username] = ['00:00.000'] * 12
        write_best_times(best_times)
        return 3

def get_leaderboard():
    high_scores = read_high_scores()
    sorted_scores = sorted(high_scores.items(), key=lambda x: x[1], reverse=True)
    leaderboard = sorted_scores[:10]
    return leaderboard

def createSmoothCorners(width, xCenter, yCenter, backColour, topColour, height=0, radius=7):
    if not(height):
        height = width
    shapes = Group()
    half_width = width / 2
    half_height = height / 2
    shapes.add(
        Rect(xCenter - half_width, yCenter + half_height, radius, radius, align = 'bottom-left', fill = backColour),
        Circle(xCenter - half_width + radius, yCenter + half_height - radius, radius, fill = topColour), 
        Rect(xCenter - half_width, yCenter - half_height, radius, radius, align='top-left', fill = backColour),
        Circle(xCenter - half_width + radius, yCenter - half_height + radius, radius, fill = topColour),
        Rect(xCenter + half_width, yCenter + half_height, radius, radius, align='bottom-right', fill = backColour),
        Circle(xCenter + half_width - radius, yCenter + half_height - radius, radius, fill = topColour),
        Rect(xCenter + half_width, yCenter - half_height, radius, radius, align='top-right', fill = backColour),
        Circle(xCenter + half_width - radius, yCenter - half_height + radius, radius, fill = topColour)
    )
    return shapes
    
def createUICornerCircles(width, xCenter, yCenter, topColour, height = 0):
    shapes = Group()
    if height == 0:
        height = width
    half_height = height / 2
    half_width = width / 2
    shapes.add(
        Circle(xCenter - half_width + 5, yCenter - half_height + 5, 5, fill = topColour),
        Circle(xCenter + half_width - 5, yCenter - half_height + 5, 5, fill = topColour)
    )
    return shapes
    
def createUICornerRect(width, xCenter, yCenter, backColour, height = 0):
    shapes = Group()
    if height == 0:
        height = width
    half_height = height / 2
    half_width = width / 2
    shapes.add(
        Rect(xCenter - half_width, yCenter - half_height, 5, 5, align='top-left', fill = backColour),
        Rect(xCenter + half_width, yCenter - half_height, 5, 5, align='top-right', fill = backColour)
    )
    return shapes

def createLeaderboard():
    outputGroup = Group()
    outputGroup.add(
        Rect(15, 15, 370, 370, fill = rgb(250, 248, 239)),
        createSmoothCorners(370, 200, 200, rgb(142, 121, 102), rgb(250, 248, 239)),
        Rect(15, 15, 370, 370, fill = rgb(250, 248, 239)),
        createSmoothCorners(370, 200, 200, rgb(142, 121, 102), rgb(250, 248, 239)),
        Rect(15, 15, 370, 50, fill = rgb(236, 231, 220)),
        createUICornerRect(370, 200, 200, rgb(142, 121, 102)),
        createUICornerCircles(370, 200, 200, rgb(236, 231, 220)),
        Label('Leaderboard', 200, 40, fill = rgb(142, 121, 102), font = 'arial', bold = True, size = 20, align = 'center'),
    )
    trophy1 = Group(
        Polygon(258, 273, 255, 281, 245, 281, 241, 292, 283, 292, 279, 281, 269, 281, 266, 273),
        Circle(262, 254, 21),
        Rect(241, 221, 42, 33),
        Arc(241, 235, 29, 32, 180, 90),
        Arc(283, 235, 29, 32, 90, 90),
        Rect(227, 224, 71, 11),
    )
    trophy2 = Group(
        Arc(241, 235, 18, 20, 180, 90, fill = 'white'),
        Arc(283, 235, 18, 20, 90, 90, fill = 'white'),
        Rect(232, 230, 9, 5, fill = 'white'),
        Rect(283, 230, 9, 5, fill = 'white'),
        Star(262, 245, 12, 5, fill = 'white')
    )
    trophy1.fill = rgb(250, 248, 239)
    trophy2.fill = rgb(142, 121, 102)
    leaderboardTrophy = Group(trophy1, trophy2)
    leaderboardTrophy.width /= 2
    leaderboardTrophy.height /= 2
    leaderboardTrophy.centerY = 100
    leaderboardTrophy.centerX = 200
    leaderboardUsernameLargestWidth = 0
    seperators = Group()
    stats = Group()
    statsBG = Group()
    leaderboard = get_leaderboard()
    for idx, (username, score) in enumerate(leaderboard, start = 0):
        if idx % 2:
            statsBG.add(Rect(25, 125 + 25 * idx, 350, 25, fill = rgb(236, 231, 220)))
        else:
            statsBG.add(Rect(25, 125 + 25 * idx, 350, 25, fill = rgb(250, 248, 239)))
        stats.add(Label(f'{idx + 1}.', 45, 125 + 25 * idx + 12.5, fill = rgb(142, 121, 102), bold = True))
        leaderboardUsernameLabel = Label(username, 75, 125 + 25 * idx + 12.5, fill = rgb(142, 121, 102), bold = True, align = 'left')
        stats.add(leaderboardUsernameLabel)
        if leaderboardUsernameLabel.width > leaderboardUsernameLargestWidth:
            leaderboardUsernameLargestWidth = leaderboardUsernameLabel.width
        seperators.add(Line(25, 125 + 25 * (idx + 1), 375, 125 + 25 * (idx + 1), fill = rgb(142, 121, 102), lineWidth = 1, opacity = 50))
    for idx, (username, score) in enumerate(leaderboard, start = 0):
        stats.add(Label(score, leaderboardUsernameLargestWidth + 30 + 65, 125 + 25 * idx + 12.5, fill = rgb(142, 121, 102), bold = True, align = 'left'))
    seperators.toFront()
    statsBG.add(seperators)
    stats.centerX = 200
    statsBG.width = stats.width + 25
    statsBG.centerX = 200
    leaderboardGroup = Group(
        Rect(200, 100, statsBG.width, 50, fill = rgb(142, 121, 102), align = 'center'),
        createUICornerRect(statsBG.width, 200, 100, rgb(250, 248, 239), 50),
        createUICornerCircles(statsBG.width, 200, 100, rgb(142, 121, 102), 50)
    )
    leaderboardGroup.add(stats, statsBG, leaderboardTrophy)
    stats.toFront()
    leaderboardTrophy.toFront()
    leaderboardGroup.centerY = 225
    outputGroup.add(leaderboardGroup)
    usernameScoreSeperator = leaderboardUsernameLargestWidth + 60 + leaderboardGroup.left
    numberUsernameSeperator = leaderboardGroup.left + 40
    outputGroup.add(
        Line(leaderboardGroup.left + 0.5, leaderboardTrophy.bottom + 8, leaderboardGroup.left + 0.5, seperators.bottom, fill = rgb(236, 231, 220), lineWidth = 1),
        Line(leaderboardGroup.right - 0.5, leaderboardTrophy.bottom + 8, leaderboardGroup.right - 0.5, seperators.bottom, fill = rgb(236, 231, 220), lineWidth = 1),
        Line(numberUsernameSeperator, leaderboardTrophy.bottom + 8, numberUsernameSeperator, seperators.bottom, fill = rgb(142, 121, 102), lineWidth = 1),
        Line(usernameScoreSeperator, leaderboardTrophy.bottom + 8, usernameScoreSeperator, seperators.bottom, fill = rgb(142, 121, 102), lineWidth = 1)
    )
    return outputGroup

def speedRunCreateSmoothCorners(width, xCenter, yCenter, backColour, topColour, height=0, radius=7):
    if not(height):
        height = width
    shapes = Group()
    half_width = width / 2
    half_height = height / 2
    shapes.add(
        Rect(xCenter - half_width, yCenter + half_height, radius, radius, align = 'bottom-left', fill = backColour),
        Circle(xCenter - half_width + radius, yCenter + half_height - radius, radius, fill = topColour), 
        Rect(xCenter - half_width, yCenter - half_height, radius, radius, align='top-left', fill = backColour),
        Circle(xCenter - half_width + radius, yCenter - half_height + radius, radius, fill = topColour),
        Rect(xCenter + half_width, yCenter + half_height, radius, radius, align='bottom-right', fill = backColour),
        Circle(xCenter + half_width - radius, yCenter + half_height - radius, radius, fill = topColour),
        Rect(xCenter + half_width, yCenter - half_height, radius, radius, align='top-right', fill = backColour),
        Circle(xCenter + half_width - radius, yCenter - half_height + radius, radius, fill = topColour)
    )
    return shapes

def speedRunCreateSideSmoothCorners(width, xCenter, yCenter, backColour, topColour, height=0, direction='r', radius=7):
    if not(height):
        height = width
    shapes = Group()
    half_width = width / 2
    half_height = height / 2
    if direction == 'l':
        shapes.add(
            Rect(xCenter - half_width, yCenter + half_height, radius, radius, align = 'bottom-left', fill = backColour),
            Circle(xCenter - half_width + radius, yCenter + half_height - radius, radius, fill = topColour), 
            Rect(xCenter - half_width, yCenter - half_height, radius, radius, align='top-left', fill = backColour),
            Circle(xCenter - half_width + radius, yCenter - half_height + radius, radius, fill = topColour)
        )
    elif direction == 'r':
        shapes.add(
            Rect(xCenter + half_width, yCenter + half_height, radius, radius, align='bottom-right', fill = backColour),
            Circle(xCenter + half_width - radius, yCenter + half_height - radius, radius, fill = topColour),
            Rect(xCenter + half_width, yCenter - half_height, radius, radius, align='top-right', fill = backColour),
            Circle(xCenter + half_width - radius, yCenter - half_height + radius, radius, fill = topColour)
        )
    return shapes

def getTileColourSpeedRun(value):
    return {
        2: rgb(238,228,218),
        4: rgb(237,224,199),
        8: rgb(242,177,122),
        16: rgb(245,149,99),
        32: rgb(246,124,96),
        64: rgb(245,95,58),
        128: rgb(241,207,95),
        256: rgb(243,203,73),
        512: rgb(243,200,44),
        1024: rgb(243,195,0),
        2048: rgb(235,184,0),
        4096: rgb(51,180,169),
        8192: rgb(39,165,154),
        16384: rgb(18,153,141),
        32768: rgb(35,167,245)
    }.get(value, rgb(235,184,0))

speedRunUI = Group(
    Rect(15, 15, 370, 370, fill = rgb(250, 248, 239)),
    speedRunCreateSmoothCorners(370, 200, 200, rgb(142, 121, 102), rgb(250, 248, 239))
)
speedRunLabel1 = Label(16, 40, 40, fill = rgb(248, 246, 242), bold = True)
speedRunLabel2 = Label(speedRunLabel1.value*2, 40, 70, fill = rgb(248, 246, 242), bold = True)
speedRunLabel3 = Label(speedRunLabel2.value*2, 40, 100, fill = rgb(248, 246, 242), bold = True)
speedRunLabels = Group(speedRunLabel1, speedRunLabel2, speedRunLabel3)
speedRunTimeLabel1 = Label('-', 82.5, 40, fill = rgb(142, 121, 102), bold = True)
speedRunTimeLabel2 = Label('-', 82.5, 70, fill = rgb(142, 121, 102), bold = True)
speedRunTimeLabel3 = Label('-', 82.5, 100, fill = rgb(142, 121, 102), bold = True)
speedRunTimeLabels = Group(speedRunTimeLabel1, speedRunTimeLabel2, speedRunTimeLabel3)
speedRunTimeTrackers = Group(
    Rect(40, 40, 70, 25, fill = rgb(240, 235, 225), align = 'left'),
    speedRunCreateSideSmoothCorners(70, 75, 40, rgb(250, 248, 239), rgb(240, 235, 225), 25),

    Rect(40, 70, 70, 25, fill = rgb(240, 235, 225), align = 'left'),
    speedRunCreateSideSmoothCorners(70, 75, 70, rgb(250, 248, 239), rgb(240, 235, 225), 25),

    Rect(40, 100, 70, 25, fill = rgb(240, 235, 225), align = 'left'),
    speedRunCreateSideSmoothCorners(70, 75, 100, rgb(250, 248, 239), rgb(240, 235, 225), 25),
)

speedRunTimeTrackerTileBG1 = Group(
    Rect(40, 40, 30, 25, fill = getTileColourSpeedRun(speedRunLabel1.value), align = 'center'),
    speedRunCreateSideSmoothCorners(30, 40, 40, rgb(250, 248, 239), getTileColourSpeedRun(speedRunLabel1.value), 25, 'l')
)
speedRunTimeTrackerTileBG2 = Group(
    Rect(40, 70, 30, 25, fill = getTileColourSpeedRun(speedRunLabel2.value), align = 'center'),
    speedRunCreateSideSmoothCorners(30, 40, 70, rgb(250, 248, 239), getTileColourSpeedRun(speedRunLabel2.value), 25, 'l')
)
speedRunTimeTrackerTileBG3 = Group(
    Rect(40, 100, 30, 25, fill = getTileColourSpeedRun(speedRunLabel3.value), align = 'center'),
    speedRunCreateSideSmoothCorners(30, 40, 100, rgb(250, 248, 239), getTileColourSpeedRun(speedRunLabel3.value), 25, 'l')
)

speedRunTimeTrackers.add(speedRunLabels, speedRunTimeLabels, speedRunTimeTrackerTileBG1, speedRunTimeTrackerTileBG2, speedRunTimeTrackerTileBG3)
speedRunTimeTrackers.centerY -= 6
speedRunTimeTrackers.centerX += 5



speedRunTime = Group(
    Rect(200, 40, 110, 40, fill = rgb(142, 121, 102), align = 'center'),
    speedRunCreateSmoothCorners(110, 200, 40, rgb(250, 248, 239), rgb(142, 121, 102), 40)
)
speedRunTimeLabel = Label('00:00.000', 200, 40, fill = rgb(255, 255, 255), size = 20, bold = True)
speedRunTime.add(speedRunTimeLabel)

speedRunScore = Group(
    Rect(200, 85, 110, 40, fill = rgb(187, 173, 159), align = 'center'),
    speedRunCreateSmoothCorners(110, 200, 85, rgb(250, 248, 239), rgb(187, 173, 159), 40)
)
speedRunScoreLabel = Label(0, 200, 85, fill = rgb(255, 255, 255), size = 20, bold = True)
speedRunScore.add(speedRunScoreLabel)

speedRunReturnToMenu = Group(
    Rect(280, 85, 35, 35, fill = rgb(129, 138, 145), align = 'center'),
    speedRunCreateSmoothCorners(35, 280, 85, rgb(250, 248, 239), rgb(129, 138, 145), radius=5),
    Line(272.5, 80, 287.5, 80, fill = rgb(250, 248, 238), lineWidth = 2),
    Line(272.5, 85, 287.5, 85, fill = rgb(250, 248, 238), lineWidth = 2),
    Line(272.5, 90, 287.5, 90, fill = rgb(250, 248, 238), lineWidth = 2)
)
speedRunReturnToMenu.centerX += 23

speedRunShowSpeedRunTimes = Group(
    Rect(330, 85, 35, 35, fill = rgb(129, 138, 145), align = 'center'),
    speedRunCreateSmoothCorners(35, 330, 85, rgb(250, 248, 239), rgb(129, 138, 145), radius=5)
)
speedRunStopWatch = Group(
    Circle(100, 290, 13, fill = None, border = rgb(250, 248, 238)),
    Arc(100, 290, 17, 17, 0, 270, fill = rgb(250, 248, 238)),
    Line(108, 280, 110, 278, fill = rgb(250, 248, 238)),
    Line(92, 280, 90, 278, fill = rgb(250, 248, 238)),
    Line(100, 277, 100, 272, fill = rgb(250, 248, 238)),
    Line(96, 272, 104, 272, fill = rgb(250, 248, 238))
)
speedRunStopWatch.width /= 1.5
speedRunStopWatch.height /= 1.5
speedRunStopWatch.centerX, speedRunStopWatch.centerY = 330, 85
speedRunShowSpeedRunTimes.add(speedRunStopWatch)
speedRunShowSpeedRunTimes.centerX += 23

speedRunRestartButton = Group(
    Rect(305, 40, 85, 35, fill = rgb(142, 121, 102), align = 'center'),
    speedRunCreateSmoothCorners(85, 305, 40, rgb(250, 248, 239), rgb(142, 121, 102), 35),
    Label('Restart', 305, 40, fill = rgb(255, 255, 255), size = 15, bold = True)
)
speedRunRestartButton.centerX += 23



speedRunUI.add(
    Rect(200, 240, 260, 260, fill = rgb(187, 173, 160), align = 'center'),
    speedRunCreateSmoothCorners(260, 200, 240, rgb(250,248,239), rgb(187,173,160))
)
numColour2_4 = rgb(119, 110, 101)
numColourOther = rgb(248, 246, 242)
app.speedRunTiles = [
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0]
]
app.speedRunTileShapes = []
for row in range(4):
    rowShapes = []
    for col in range(4):
        xCenter = 70 + 10 * (row + 1) + 52.5 * row
        yCenter = 110 + 10 * (col + 1) + 52.5 * col
        rect = Rect(xCenter, yCenter, 52.5, 52.5, fill = rgb(205, 193, 180))
        xCenter += 26.25
        yCenter += 26.25
        cornerRects = Group(
            Rect(xCenter - 26.25, yCenter + 26.25, 5, 5, align = 'bottom-left', fill = rgb(187, 173, 160)),
            Rect(xCenter - 26.25, yCenter - 26.25, 5, 5, align = 'top-left', fill = rgb(187, 173, 160)),
            Rect(xCenter + 26.25, yCenter + 26.25, 5, 5, align = 'bottom-right', fill = rgb(187, 173, 160)),
            Rect(xCenter + 26.25, yCenter - 26.25, 5, 5, align = 'top-right', fill = rgb(187, 173, 160))
        )
        cornerCircles = Group(
            Circle(xCenter - 21.25, yCenter + 21.25, 5, fill = rgb(205, 193, 180)), 
            Circle(xCenter - 21.25, yCenter - 21.25, 5, fill = rgb(205, 193, 180)),
            Circle(xCenter + 21.25, yCenter + 21.25, 5, fill = rgb(205, 193, 180)),
            Circle(xCenter + 21.25, yCenter - 21.25, 5, fill = rgb(205, 193, 180))
        )
        label = Label('', xCenter, yCenter, fill = numColour2_4, size = 17.5, font = 'arial', bold = True)
        rowShapes.append((rect, label, cornerCircles, cornerRects))
    app.speedRunTileShapes.append(rowShapes)


def drawTilesSpeedRun():
    for row in range(4):
        for col in range(4):
            num = app.speedRunTiles[row][col]
            rect, label, cornerCircles, cornerRects = app.speedRunTileShapes[row][col]
            if num == 0:
                rect.fill = rgb(205, 193, 180)
                cornerCircles.fill = rgb(205, 193, 180)
                label.value = ''
            else:
                rect.fill = getTileColourSpeedRun(num)
                cornerCircles.fill = getTileColourSpeedRun(num)
                label.value = num
                label.fill = numColour2_4 if num in [2, 4] else numColourOther

def addRandomTileSpeedRun():
    emptyTiles = []
    for row in range(4):
        for col in range(4):
            if app.speedRunTiles[row][col] == 0:
                emptyTiles.append((row, col))
    if emptyTiles:
        row, col = random.choice(emptyTiles)
        if random.random() < 0.9:
            app.speedRunTiles[row][col] = 2
        else:
            app.speedRunTiles[row][col] = 4

def mergeSpeedRun(row):
    merged_row = []
    for num in row:
        if num != 0:
            merged_row.append(num)
    for item in range(len(merged_row) - 1):
        if merged_row[item] == merged_row[item + 1]:
            merged_row[item] *= 2
            speedRunScoreLabel.value += merged_row[item]
            merged_row[item + 1] = 0
    merged_row = [num for num in merged_row if num != 0]
    return merged_row + [0] * (4 - len(merged_row))

def moveUpSpeedRun():
    moved = False
    new_tiles = []
    for row in range(4):
        newRow = mergeSpeedRun(app.speedRunTiles[row])
        if newRow != app.speedRunTiles[row]:
            moved = True
        new_tiles.append(newRow)
    app.speedRunTiles = new_tiles
    return moved

def moveDownSpeedRun():
    moved = False
    new_tiles = []
    for row in range(4):
        newRow = list(reversed(mergeSpeedRun(reversed(app.speedRunTiles[row]))))
        if newRow != app.speedRunTiles[row]:
            moved = True
        new_tiles.append(newRow)
    app.speedRunTiles = new_tiles
    return moved

def moveLeftSpeedRun():
    moved = False
    col_tuples = zip(*app.speedRunTiles)
    transposed_tiles = [list(column) for column in col_tuples]
    app.speedRunTiles = transposed_tiles
    if moveUpSpeedRun():
        moved = True
    row_tuples = zip(*app.speedRunTiles)
    transposed_tiles = [list(row) for row in row_tuples]
    app.speedRunTiles = transposed_tiles
    return moved

def moveRightSpeedRun():
    moved = False
    col_tuples = zip(*app.speedRunTiles)
    transposed_tiles = [list(column) for column in col_tuples]
    app.speedRunTiles = transposed_tiles
    if moveDownSpeedRun():
        moved = True
    row_tuples = zip(*app.speedRunTiles)
    transposed_tiles = [list(row) for row in row_tuples]
    app.speedRunTiles = transposed_tiles
    return moved

def checkGameOverSpeedRun():
    for row in app.speedRunTiles:
        if 0 in row: 
            return 'continue'
    for row in app.speedRunTiles:
        for item in range(3):
            if row [item] == row[item + 1]:
                return 'continue'
    for col in range(4):
        for row in range(3):
            if app.speedRunTiles[row][col] == app.speedRunTiles[row + 1][col]:
                return 'continue'
    app.gridIsFull = True
    app.hasStartedSpeedRunning = False
    return 'lose'


def checkForValueInGrid():
    for row in app.speedRunTiles:
        if app.currentlyCheckingFor in row:
            app.currentlyCheckingFor *= 2
            return True
        else:
            return False

speedRunGameOverScreen = Group(
    Rect(200, 240, 260, 260, fill = rgb(250, 248, 239), align = 'center', opacity = 75)
)
speedRunTryAgainButton = Group(
    Rect(200, 280, 150, 50, fill = rgb(142, 121, 102), align = 'center'),
    speedRunCreateSmoothCorners(150, 200, 280, rgb(227, 221, 209), rgb(142, 121, 102), 50),
    Label('Try Again?', 200, 280, fill = rgb(249, 246, 242), size = 20, font = 'arial')
)
speedRunGameOverScreenResult = Label('', 200, 180, size = 25, fill = rgb(143, 120, 101), font = 'arial', bold = True)
speedRunGameOverScreenScore = Label('', 200, 220, size = 20, fill = rgb(143, 120, 101), font = 'arial')
speedRunGameOverScreen.add(speedRunTryAgainButton, speedRunGameOverScreenResult, speedRunGameOverScreenScore)
speedRunGameOverScreen.visible = False

def showGameOverScreenSpeedRun(result):
    speedRunGameOverScreen.visible = True
    if result =='win':
        speedRunGameOverScreenResult.value = 'You Win'
    elif result =='lose':
        speedRunGameOverScreenResult.value ='Game Over!'
    speedRunGameOverScreenScore.value = f'Your Score: {speedRunScoreLabel.value}'

def createSpeedRunTime(xCenter, yCenter, num, numTime):
    shapes = Group()
    shapes.add(
        Rect(xCenter + 23, yCenter, 87, 40, fill = rgb(240, 235, 225), align = 'center'),
        speedRunCreateSideSmoothCorners(87, xCenter + 23, yCenter, rgb(250, 248, 239), rgb(240, 235, 225), 40, 'r', 10),
        Rect(xCenter - 43, yCenter, 47, 40, fill = getTileColourSpeedRun(num), align = 'center'),
        speedRunCreateSideSmoothCorners(47, xCenter - 43, yCenter, rgb(250, 248, 239), getTileColourSpeedRun(num), 40, 'l', 10),
    )
    if numTime == '00:00.000':
        numTime = '-'
    shapes.add(
        Label(str(numTime), xCenter + 23, yCenter, fill = rgb(142, 121, 102), bold = True, size = 12),
        Label(str(num), xCenter - 43, yCenter, fill = rgb(248, 246, 242), bold = True, size = 12)
    )
    return shapes

def createSpeedRunLeaderboard(username):
    shapes = Group(
        Rect(200, 200, 370, 370, fill = rgb(250, 249, 238), align = 'center'),
        speedRunCreateSmoothCorners(370, 200, 200, rgb(142, 121, 102), rgb(250, 248, 239), radius = 10),
        Rect(15, 15, 370, 370, fill = rgb(250, 248, 239)),
        speedRunCreateSmoothCorners(370, 200, 200, rgb(142, 121, 102), rgb(250, 248, 239)),
        Rect(15, 15, 370, 50, fill = rgb(236, 231, 220)),
        createUICornerRect(370, 200, 200, rgb(142, 121, 102)),
        createUICornerCircles(370, 200, 200, rgb(236, 231, 220)),
        Label('Your Best Speed Runs', 200, 40, fill = rgb(142, 121, 102), font = 'arial', bold = True, size = 20)
    )
    best_times = read_best_times()
    timeList = best_times[username]
    tempValue = 16
    for col in range(1, 3):
        for row in range(1, 7):
            if col == 1:
                shapes.add(createSpeedRunTime(110, 89 + 40 * (row - 1) + 10 * row, tempValue, timeList[(row - 1)]))
            else:
                shapes.add(createSpeedRunTime(290, 89 + 40 * (row - 1) + 10 * row, tempValue, timeList[6 + (row - 1)]))
            tempValue *= 2
    return shapes

def resetGameSpeedRun(username):
    app.speedRunTiles = [
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0]
    ]
    addRandomTileSpeedRun()
    addRandomTileSpeedRun()
    speedRunScoreLabel.value = 0
    speedRunTimeLabel.value = '00:00.000'
    speedRunTimeLabel1.value = '-'
    speedRunTimeLabel2.value = '-'
    speedRunTimeLabel3.value = '-'
    speedRunLabel1.value = 16
    speedRunLabel2.value = 32
    speedRunLabel3.value = 64
    speedRunTimeTrackerTileBG1.clear()
    speedRunTimeTrackerTileBG1.add(
        Rect(40, 40, 30, 25, fill = getTileColourSpeedRun(speedRunLabel1.value), align = 'center'),
        speedRunCreateSideSmoothCorners(30, 40, 40, rgb(250, 248, 239), getTileColourSpeedRun(speedRunLabel1.value), 25, 'l')
    )
    speedRunTimeTrackerTileBG2.clear()
    speedRunTimeTrackerTileBG2.add(
        Rect(40, 70, 30, 25, fill = getTileColourSpeedRun(speedRunLabel2.value), align = 'center'),
        speedRunCreateSideSmoothCorners(30, 40, 70, rgb(250, 248, 239), getTileColourSpeedRun(speedRunLabel2.value), 25, 'l')
    )
    speedRunTimeTrackerTileBG3.clear()
    speedRunTimeTrackerTileBG3.add(
        Rect(40, 100, 30, 25, fill = getTileColourSpeedRun(speedRunLabel3.value), align = 'center'),
        speedRunCreateSideSmoothCorners(30, 40, 100, rgb(250, 248, 239), getTileColourSpeedRun(speedRunLabel3.value), 25, 'l')
    )
    speedRunTimeTrackerTileBG1.centerY -= 6
    speedRunTimeTrackerTileBG1.centerX += 5
    speedRunTimeTrackerTileBG2.centerY -= 6
    speedRunTimeTrackerTileBG2.centerX += 5
    speedRunTimeTrackerTileBG3.centerY -= 6
    speedRunTimeTrackerTileBG3.centerX += 5
    speedRunLabels.toFront()
    drawTilesSpeedRun()
    if username != 'Guest':
        app.newTime += ['00:00.000'] * (12 - len(app.newTime))
        update_best_times(username, app.newTime)
        app.newTime = []
    speedRunGameOverScreen.visible = False
    app.gridIsFull = False
    app.hasStartedSpeedRunning = False
    app.currentlyCheckingFor = 16

Rect(15, 15, 370, 370, fill = rgb(250, 248, 239))
createSmoothCorners(370, 200, 200, rgb(142, 121, 102), rgb(250, 248, 239))
mainMenu = Group(
    Rect(15, 15, 370, 370, fill = rgb(250, 248, 239)),
    createSmoothCorners(370, 200, 200, rgb(142, 121, 102), rgb(250, 248, 239)),
    Rect(15, 15, 370, 50, fill = rgb(236, 231, 220)),
    createUICornerRect(370, 200, 200, rgb(142, 121, 102)),
    createUICornerCircles(370, 200, 200, rgb(236, 231, 220)),
    Label('2048', 30, 40, fill = rgb(142, 121, 102), font = 'arial', bold = True, size = 20, align = 'left')
)

trophy1 = Group(
    Polygon(258, 273, 255, 281, 245, 281, 241, 292, 283, 292, 279, 281, 269, 281, 266, 273),
    Circle(262, 254, 21),
    Rect(241, 221, 42, 33),
    Arc(241, 235, 29, 32, 180, 90),
    Arc(283, 235, 29, 32, 90, 90),
    Rect(227, 224, 71, 11),
)
trophy2 = Group(
    Arc(241, 235, 18, 20, 180, 90, fill = 'white'),
    Arc(283, 235, 18, 20, 90, 90, fill = 'white'),
    Rect(232, 230, 9, 5, fill = 'white'),
    Rect(283, 230, 9, 5, fill = 'white'),
    Star(262, 245, 12, 5, fill = 'white')
)

trophy3 = Group(
    Polygon(258, 273, 255, 281, 245, 281, 241, 292, 283, 292, 279, 281, 269, 281, 266, 273),
    Circle(262, 254, 21),
    Rect(241, 221, 42, 33),
    Arc(241, 235, 29, 32, 180, 90),
    Arc(283, 235, 29, 32, 90, 90),
    Rect(227, 224, 71, 11)
)
trophy4 = Group(
    Arc(241, 235, 18, 20, 180, 90, fill = 'white'),
    Arc(283, 235, 18, 20, 90, 90, fill = 'white'),
    Rect(232, 230, 9, 5, fill = 'white'),
    Rect(283, 230, 9, 5, fill = 'white'),
    Star(262, 245, 12, 5, fill = 'white')
)
mainMenuHighScoreLabel = Label('Play to get a high score', 275, 248, fill = rgb(142,121,102), bold = True, align = 'left')


usernameBox = Group(
    Rect(200, 150, 250, 50, fill = rgb(238, 228, 218), align = 'center'),
    createSmoothCorners(250, 200, 150, rgb(250, 248, 239), rgb(238, 228, 218), 50),
)
usernameLabel = Label('Guest', 200, 150, size = 18, fill = rgb(142, 121, 102), bold = True)
usernameBox.add(usernameLabel)
personImage = Image('PersonImage.png', 200, 200)
personImage.height /= 3
personImage.width /= 3
personImage.centerX = 100
personImage.centerY = 150
usernameBox.add(personImage)

classicGameButton = Group(
    Rect(200, 220, 250, 50, fill = rgb(142, 121, 102), align = 'center'),
    createSmoothCorners(250, 200, 220, rgb(250, 248, 239), rgb(142, 121, 102), 50),
    Label('Classic 2048', 145, 220, size = 18, fill = 'white', bold = True, align = 'left'),
    Rect(75, 195, 50, 50, fill = rgb(122, 104, 88)),
    createSmoothCorners(50, 100, 220, rgb(250, 248, 239), rgb(122, 104, 88)),
    Rect(115, 195, 10, 50, fill = rgb(122, 104, 88)),
)
playImage = Image('GamePlayImage.png', 200, 200)
playImage.height /= 3.5
playImage.width /= 3.5
playImage.centerX = 100
playImage.centerY = 220
classicGameButton.add(playImage)


speedunButton = Group(
    Rect(200, 290, 250, 50, fill = rgb(216, 216, 216), align = 'center'),
    createSmoothCorners(250, 200, 290, rgb(250, 248, 239), rgb(216, 216, 216), 50),
    Label('Speedrun', 145, 290, size = 18, fill = rgb(113, 112, 112), bold = True, align = 'left'),
    Rect(75, 265, 50, 50, fill = rgb(186, 186, 186)),
    createSmoothCorners(50, 100, 290, rgb(250, 248, 239), rgb(186, 186, 186)),
    Rect(115, 265, 10, 50, fill = rgb(186, 186, 186))
)
stopWatch = Group(
    Circle(100, 290, 13, fill = None, border = rgb(113, 112, 112)),
    Arc(100, 290, 17, 17, 0, 270, fill = rgb(113, 112, 112)),
    Line(108, 280, 110, 278, fill = rgb(113, 112, 112)),
    Line(92, 280, 90, 278, fill = rgb(113, 112, 112)),
    Line(100, 277, 100, 272, fill = rgb(113, 112, 112)),
    Line(96, 272, 104, 272, fill = rgb(113, 112, 112))
)
stopWatch.centerY = 290
speedunButton.add(stopWatch)


trophy = Group(trophy1, trophy2)
trophy.height /= 2.8
trophy.width /= 2.8
trophy.centerX = 355
trophy.centerY = 40
trophy1.fill = rgb(142,121,102)
trophy2.fill = rgb(236, 231, 220)

trophyAndHighScore = Group()
highScoreTrophy = Group(trophy3, trophy4)
highScoreTrophy.height /= 5
highScoreTrophy.width /= 5
trophy3.fill = rgb(217, 83, 79)
trophy4.fill = rgb(250, 248, 239)
trophyAndHighScore.add(highScoreTrophy, mainMenuHighScoreLabel)
highScoreTrophy.right = mainMenuHighScoreLabel.left - 10
trophyAndHighScore.centerX = 200
trophyAndHighScore.centerY = 40

signInButton = Group(
    Rect(200, 360, 250, 50, fill = rgb(118, 196, 125), align = 'center'),
    createSmoothCorners(250, 200, 360, rgb(250, 248, 239), rgb(118, 196, 125), 50),
    Label('Sign In', 145, 360, size = 18, fill = rgb(255, 255, 255), bold = True, align = 'left'),
    Rect(75, 335, 50, 50, fill = rgb(101, 168, 107)),
    createSmoothCorners(50, 100, 360, rgb(250, 248, 239), rgb(101, 168, 107)),
    Rect(115, 335, 10, 50, fill = rgb(101, 168, 107))
)
signInImage = Image('SignInImage.png', 200, 200)
signInImage.height /= 4.5
signInImage.width /= 4.5
signInImage.centerX = 100
signInImage.centerY = 360
signInButton.add(signInImage)



selector = Group(
    Polygon(15, 210, 30, 220, 15, 230, fill = rgb(142, 121, 102)),
    Polygon(385, 210, 370, 220, 385, 230, fill = rgb(142, 121, 102))
)
selector.position = 2
buttons = Group()
buttons.add(usernameBox, classicGameButton, speedunButton, selector, signInButton)
buttons.centerY -= 30
mainMenu.add(trophy, trophyAndHighScore, usernameBox, classicGameButton, speedunButton, selector, signInButton)
mainMenu.toFront()


signInScreen = Group(
    Rect(15, 15, 370, 370, fill = rgb(250, 248, 239)),
    createSmoothCorners(370, 200, 200, rgb(142, 121, 102), rgb(250, 248, 239)),
    Rect(15, 15, 370, 50, fill = rgb(236, 231, 220)),
    createUICornerRect(370, 200, 200, rgb(142, 121, 102)),
    createUICornerCircles(370, 200, 200, rgb(236, 231, 220)),
    Label('Sign Up / Login', 200, 40, fill = rgb(142, 121, 102), font = 'arial', bold = True, size = 20)
)

signInScreenUsername = Group(
    Rect(200, 150, 250, 50, fill = rgb(238, 228, 218), align = 'center'),
    createSmoothCorners(250, 200, 150, rgb(250, 248, 239), rgb(238, 228, 218), 50)
)
signInUsernameLabel = Label('username', 200, 150, size = 15, fill = rgb(170, 150, 130), bold = True)
signInScreenUsername.add(signInUsernameLabel)

signInScreenPassword = Group(
    Rect(200, 220, 250, 50, fill = rgb(238, 228, 218), align = 'center'),
    createSmoothCorners(250, 200, 220, rgb(250, 248, 239), rgb(238, 228, 218), 50)
)
signInPasswordLabel = Label('password', 200, 220, size = 15, fill = rgb(170, 150, 130), bold = True)
signInScreenPassword.add(signInPasswordLabel)

signInScreenSubmitButton = Group(
    Rect(200, 290, 250, 50, fill = rgb(238, 228, 218), align = 'center'),
    createSmoothCorners(250, 200, 290, rgb(250, 248, 239), rgb(238, 228, 218), 50),
    Label('Submit', 200, 290, size = 18, fill = rgb(142, 121, 102), bold = True)
)

signInOptionSelector = Group(
    Polygon(15, 140, 30, 150, 15, 160, fill = rgb(142, 121, 102)),
    Polygon(385, 140, 370, 150, 385, 160, fill = rgb(142, 121, 102))
)

signInOptionSelector.position = 1
signInScreen.add(signInScreenUsername, signInScreenPassword, signInOptionSelector, signInScreenSubmitButton)

signInScreen.visible = False

signInScreenResultOutputGroup1 = Group(
        Rect(15, 15, 370, 370, fill = rgb(250, 248, 239)),
        createSmoothCorners(370, 200, 200, rgb(142, 121, 102), rgb(250, 248, 239)),
        Rect(15, 15, 370, 50, fill = rgb(236, 231, 220)),
        createUICornerRect(370, 200, 200, rgb(142, 121, 102)),
        createUICornerCircles(370, 200, 200, rgb(236, 231, 220)),
        Label('Sign Up / Login', 200, 40, fill = rgb(142, 121, 102), font = 'arial', bold = True, size = 20),
        Label('Welcome Back,', 200, 180, fill = rgb(142, 121, 102), size = 20, bold = True)
)
signInScreenResultOutputGroup1Username = Label('', 200, 220, fill = rgb(142, 121, 102), size = 20, bold = True, italic = True)
signInScreenResultOutputGroup1.add(signInScreenResultOutputGroup1Username)
signInScreenResultOutputGroup1.visible = False

signInScreenResultOutputGroup2 = Group(
        Rect(15, 15, 370, 370, fill = rgb(250, 248, 239)),
        createSmoothCorners(370, 200, 200, rgb(142, 121, 102), rgb(250, 248, 239)),
        Rect(15, 15, 370, 50, fill = rgb(236, 231, 220)),
        createUICornerRect(370, 200, 200, rgb(142, 121, 102)),
        createUICornerCircles(370, 200, 200, rgb(236, 231, 220)),
        Label('Sign Up / Login', 200, 40, fill = rgb(142, 121, 102), font = 'arial', bold = True, size = 20),
        Label('Incorrect Password for', 200, 180, fill = rgb(142, 121, 102), size = 20, bold = True)
)
signInScreenResultOutputGroup2Username = Label('', 200, 220, fill = rgb(142, 121, 102), size = 20, bold = True, italic = True)
signInScreenResultOutputGroup2.add(signInScreenResultOutputGroup2Username)
signInScreenResultOutputGroup2.visible = False

signInScreenResultOutputGroup3 = Group(
        Rect(15, 15, 370, 370, fill = rgb(250, 248, 239)),
        createSmoothCorners(370, 200, 200, rgb(142, 121, 102), rgb(250, 248, 239)),
        Rect(15, 15, 370, 50, fill = rgb(236, 231, 220)),
        createUICornerRect(370, 200, 200, rgb(142, 121, 102)),
        createUICornerCircles(370, 200, 200, rgb(236, 231, 220)),
        Label('Sign Up / Login', 200, 40, fill = rgb(142, 121, 102), font = 'arial', bold = True, size = 20),
        Label('Account Created Successfully', 200, 160, fill = rgb(142, 121, 102), size = 20, bold = True),
        Label('Welcome,', 200, 200, fill = rgb(142, 121, 102), size = 20, bold = True)
)
signInScreenResultOutputGroup3Username = Label('', 200, 260, fill = rgb(142, 121, 102), size = 20, bold = True, italic = True)
signInScreenResultOutputGroup3.add(signInScreenResultOutputGroup3Username)
signInScreenResultOutputGroup3.visible = False

resetButton = Group(
    Rect(80, 70, 70, 70, fill = rgb(142,121,102), align = 'center'),
    createSmoothCorners(70, 80, 70, rgb(250, 248, 239), rgb(142,121,102)),
    Circle(80, 70, 21.875, fill = None, border = rgb(250, 248, 239), borderWidth = 2.625),
    Rect(79, 69, 20.875, 20.875, fill = rgb(142,121,102), align = 'bottom-right'),
    RegularPolygon(79, 49.125, 7.875, 3, rotateAngle = 30, fill = rgb(250, 248, 239))
)

scoreBox = Group(
    Rect(200, 70, 70, 70, fill = rgb(142,121,102), align = 'center'),
    createSmoothCorners(70, 200, 70, rgb(250, 248, 239), rgb(142,121,102)),
    Label('Score', 200, 54.25, fill = rgb(250, 248, 239), size = 17.5, font = 'arial', bold = True)
)
score = Label(0, 200, 83.125, fill = rgb(250, 248, 239), size = 21.875, font = 'arial', bold = False)
scoreBox.add(score)

highScoreBox = Group(
    Rect(320, 70, 70, 70, fill = rgb(142,121,102), align = 'center'),
    createSmoothCorners(70, 320, 70, rgb(250, 248, 239), rgb(142,121,102)),
    Label('High Score', 320, 54.25, fill = rgb(250, 248, 239), size = 11.666, font = 'arial', bold = True)
)
highScore = Label(0, 320, 83.125, fill = rgb(250, 248, 239), size = 21.875, font = 'arial', bold = False)
highScoreBox.add(highScore)
resetButton.centerY -= 8
resetButton.centerX += 15
scoreBox.centerY -= 8
highScoreBox.centerY -= 8
highScoreBox.centerX -= 15

Rect(200, 240, 260, 260, fill = rgb(187, 173, 160), align = 'center')
createSmoothCorners(260, 200, 240, rgb(250,248,239), rgb(187,173,160))
numColour2_4 = rgb(119, 110, 101)
numColourOther = rgb(248, 246, 242)
app.tiles = [
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0]
]
app.tileShapes = []
for row in range(4):
    rowShapes = []
    for col in range(4):
        xCenter = 70 + 10 * (row + 1) + 52.5 * row
        yCenter = 110 + 10 * (col + 1) + 52.5 * col
        rect = Rect(xCenter, yCenter, 52.5, 52.5, fill = rgb(205, 193, 180))
        xCenter += 26.25
        yCenter += 26.25
        Rect(xCenter - 26.25, yCenter + 26.25, 5, 5, align = 'bottom-left', fill = rgb(187, 173, 160)),
        Rect(xCenter - 26.25, yCenter - 26.25, 5, 5, align = 'top-left', fill = rgb(187, 173, 160)),
        Rect(xCenter + 26.25, yCenter + 26.25, 5, 5, align = 'bottom-right', fill = rgb(187, 173, 160)),
        Rect(xCenter + 26.25, yCenter - 26.25, 5, 5, align = 'top-right', fill = rgb(187, 173, 160))
        cornerCircles = Group(
            Circle(xCenter - 21.25, yCenter + 21.25, 5, fill = rgb(205, 193, 180)), 
            Circle(xCenter - 21.25, yCenter - 21.25, 5, fill = rgb(205, 193, 180)),
            Circle(xCenter + 21.25, yCenter + 21.25, 5, fill = rgb(205, 193, 180)),
            Circle(xCenter + 21.25, yCenter - 21.25, 5, fill = rgb(205, 193, 180))
        )
        label = Label('', xCenter, yCenter, fill = numColour2_4, size = 17.5, font = 'arial', bold = True)
        rowShapes.append((rect, label, cornerCircles))
    app.tileShapes.append(rowShapes)
gameOverScreen = Group(
    Rect(200, 240, 260, 260, fill = rgb(250, 248, 239), align = 'center', opacity = 75)
)
tryAgainButton = Group(
    Rect(200, 280, 150, 50, fill = rgb(142, 121, 102), align = 'center'),
    createSmoothCorners(150, 200, 280, rgb(227, 221, 209), rgb(142, 121, 102), 50),
    Label('Try Again?', 200, 280, fill = rgb(249, 246, 242), size = 20, font = 'arial')
)
gameOverScreenResult = Label('', 200, 180, size = 25, fill = rgb(143, 120, 101), font = 'arial', bold = True)
gameOverScreenScore = Label('', 200, 220, size = 20, fill = rgb(143, 120, 100), font = 'arial')
gameOverScreen.add(tryAgainButton, gameOverScreenResult, gameOverScreenScore)
gameOverScreen.visible = False

def changeSpeedRunGameVisibility(visibilityBool = False):
    if not(visibilityBool):
        resetGameSpeedRun(usernameLabel.value)
    speedRunUI.visible = visibilityBool
    speedRunTimeTrackerTileBG1.visible = visibilityBool
    speedRunTimeTrackerTileBG2.visible = visibilityBool
    speedRunTimeTrackerTileBG3.visible = visibilityBool
    speedRunTimeTrackers.visible = visibilityBool
    speedRunTime.visible = visibilityBool
    speedRunScore.visible = visibilityBool
    speedRunReturnToMenu.visible = visibilityBool
    speedRunShowSpeedRunTimes.visible = visibilityBool
    speedRunRestartButton.visible = visibilityBool
    if visibilityBool:
        speedRunUI.toFront()
        speedRunTimeTrackerTileBG1.toFront()
        speedRunTimeTrackerTileBG2.toFront()
        speedRunTimeTrackerTileBG3.toFront()
        speedRunTimeTrackers.toFront()
        speedRunLabels.toFront()
        speedRunTime.toFront()
        speedRunScore.toFront()
        speedRunReturnToMenu.toFront()
        speedRunShowSpeedRunTimes.toFront()
        speedRunRestartButton.toFront()
    elif not(visibilityBool):
        speedRunUI.toBack()
        speedRunTimeTrackerTileBG1.toBack()
        speedRunTimeTrackerTileBG2.toBack()
        speedRunTimeTrackerTileBG3.toBack()
        speedRunTimeTrackers.toBack()
        speedRunLabels.toBack()
        speedRunTime.toBack()
        speedRunScore.toBack()
        speedRunReturnToMenu.toBack()
        speedRunShowSpeedRunTimes.toBack()
        speedRunRestartButton.toBack()
    for row in range(4):
        for col in range(4):
            app.speedRunTiles[row][col]
            rect, label, cornerCircles, cornerRects = app.speedRunTileShapes[row][col]
            rect.visible = visibilityBool
            label.visible = visibilityBool
            cornerCircles.visible = visibilityBool
            cornerRects.visible = visibilityBool
            if visibilityBool:
                rect.toFront()
                label.toFront()
                cornerRects.toFront()
                cornerCircles.toFront()
            elif not(visibilityBool):
                rect.toBack()
                label.toBack()
                cornerRects.toBack()
                cornerCircles.toBack()
changeSpeedRunGameVisibility(False)


def drawTiles():
    for row in range(4):
        for col in range(4):
            num = app.tiles[row][col]
            rect, label, cornerCircles = app.tileShapes[row][col]
            if num == 0:
                rect.fill = rgb(205, 193, 180)
                cornerCircles.fill = rgb(205, 193, 180)
                label.value = ''
            else:
                rect.fill = getTileColour(num)
                cornerCircles.fill = getTileColour(num)
                label.value = num
                label.fill = numColour2_4 if num in [2, 4] else numColourOther

def getTileColour(value):
    return {
        2: rgb(238,228,218),
        4: rgb(237,224,199),
        8: rgb(242,177,122),
        16: rgb(245,149,99),
        32: rgb(246,124,96),
        64: rgb(245,95,58),
        128: rgb(241,207,95),
        256: rgb(243,200,44),
        512: rgb(243,200,44),
        1024: rgb(243,195,0),
        2048: rgb(235,184,0),
        4096: rgb(51,180,169),
        8192: rgb(39,165,154),
        16384: rgb(18,153,141),
        32768: rgb(35,167,245)
    }.get(value, rgb(235,184,0))

def addRandomTile():
    emptyTiles = []
    for row in range(4):
        for col in range(4):
            if app.tiles[row][col] == 0:
                emptyTiles.append((row, col))
    if emptyTiles:
        row, col = random.choice(emptyTiles)
        if random.random() < 0.9:
            app.tiles[row][col] = 2
        else:
            app.tiles[row][col] = 4

def merge(row):
    merged_row = []
    for num in row:
        if num != 0:
            merged_row.append(num)
    for item in range(len(merged_row) - 1):
        if merged_row[item] == merged_row[item + 1]:
            merged_row[item] *= 2
            score.value += merged_row[item]
            if score.value > highScore.value:
                highScore.value = score.value
                mainMenuHighScoreLabel.value = score.value
                highScoreTrophy.right = mainMenuHighScoreLabel.left - 10
                resultNotNeeded = submit_high_score(usernameLabel.value, highScore.value)
            merged_row[item + 1] = 0
    merged_row = [num for num in merged_row if num != 0]
    return merged_row + [0] * (4 - len(merged_row))

def moveUp():
    moved = False
    new_tiles = []
    for row in range(4):
        newRow = merge(app.tiles[row])
        if newRow != app.tiles[row]:
            moved = True
        new_tiles.append(newRow)
    app.tiles = new_tiles
    return moved

def moveDown():
    moved = False
    new_tiles = []
    for row in range(4):
        newRow = list(reversed(merge(reversed(app.tiles[row]))))
        if newRow != app.tiles[row]:
            moved = True
        new_tiles.append(newRow)
    app.tiles = new_tiles
    return moved

def moveLeft():
    moved = False
    col_tuples = zip(*app.tiles)
    transposed_tiles = [list(column) for column in col_tuples]
    app.tiles = transposed_tiles
    if moveUp():
        moved = True
    row_tuples = zip(*app.tiles)
    transposed_tiles = [list(row) for row in row_tuples]
    app.tiles = transposed_tiles
    return moved

def moveRight():
    moved = False
    col_tuples = zip(*app.tiles)
    transposed_tiles = [list(column) for column in col_tuples]
    app.tiles = transposed_tiles
    if moveDown():
        moved = True
    row_tuples = zip(*app.tiles)
    transposed_tiles = [list(row) for row in row_tuples]
    app.tiles = transposed_tiles
    return moved

def checkGameOver():
    for row in app.tiles:
        if 0 in row: 
            return 'continue'
    for row in app.tiles:
        for item in range(3):
            if row [item] == row[item + 1]:
                return 'continue'
    for col in range(4):
        for row in range(3):
            if app.tiles[row][col] == app.tiles[row + 1][col]:
                return 'continue'
    return 'lose'

def showGameOverScreen(result):
    gameOverScreen.visible = True
    if result =='win':
        gameOverScreenResult.value = 'You Win'
    elif result =='lose':
        gameOverScreenResult.value ='Game Over!'
    gameOverScreenScore.value = f'Your Score:{score.value}'

def setupBoardForTesting(testType = 0):
    if testType == 'full':
        app.tiles = [
            [2, 16, 4, 256],
            [4, 64, 16, 8],
            [64, 32, 64, 8],
            [8, 4, 128, 2]
        ]
    elif testType != 0:
        app.tiles = [
            [int(testType/2),int(testType/2),0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]
        ]
    drawTiles()    

def resetGame(testing = None):
    app.tiles = [
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0]
    ]
    addRandomTile()
    addRandomTile()
    score.value = 0
    drawTiles()
    gameOverScreen.visible = False
    if testing:
        setupBoardForTesting(testing)

def onKeyPress(key):
    if app.inClassicGame:
        if key == 'escape':
            app.inClassicGame = False
            app.inSpeedRunGame = False
            app.inMainMenu = True
            mainMenu.visible = True
            mainMenu.toFront()
        if key == 'r':
            resetGame()
            return
        if key == 'f':
            resetGame('full')
            return
        if key == '0':
            resetGame(2048)
            return
        if key == '1':
            resetGame(4096)
            return
        if key == '2':
            resetGame(8192)
            return
        if key == '3':
            resetGame(16384)
            return
        if key == '4':
            resetGame(32768)
            return
        result = checkGameOver()
        if result != 'continue':
            showGameOverScreen(result)
            return
        moved = False
        if key == 'up' or key == 'w':
            moved = moveUp()
        if key == 'down' or key == 's':
            moved = moveDown()
        if key == 'left' or key == 'a':
            moved = moveLeft()
        if key == 'right' or key == 'd':
            moved = moveRight()
        if moved:
            addRandomTile()
        drawTiles()
        result = checkGameOver()
        if result != 'continue':
            showGameOverScreen(result)


    
    if app.isEditingSignUpUsername:
        invalidKeys = ['up', 'down', 'left', 'right', 'tab', 'escape']
        if key == 'backspace':
            currentSignInUsernameValue = signInUsernameLabel.value[:-2]
            signInUsernameLabel.value = f'{currentSignInUsernameValue}_'
        elif key == 'enter':
            app.justExitedSignUpEditingMode = True
            currentSignInUsernameValue = signInUsernameLabel.value[:-1]
            signInUsernameLabel.value = currentSignInUsernameValue
            app.isEditingSignUpUsername = False
            app.isSigningIn = True
            if signInUsernameLabel.value == 'usename' or signInUsernameLabel.value == '':
                signInUsernameLabel.fill = rgb(170, 150, 130)
                signInUsernameLabel.size = 15
                signInUsernameLabel.value = 'username'
        elif key == 'space':
            currentSignInUsernameValue = signInUsernameLabel.value[:-1]
            signInUsernameLabel.value = f'{currentSignInUsernameValue} _'
        elif signInUsernameLabel.width < 190 and not(key in invalidKeys):
            currentSignInUsernameValue = signInUsernameLabel.value[:-1]
            signInUsernameLabel.value = f'{currentSignInUsernameValue}{key}_'
        if key == 'escape':
            app.justExitedSignUpEditingMode = True
            currentSignInUsernameValue = signInUsernameLabel.value[:-1]
            signInUsernameLabel.value = currentSignInUsernameValue
            app.isEditingSignUpUsername = False
            app.isSigningIn = True
            if signInUsernameLabel.value == 'username' or signInUsernameLabel.value == '':
                signInUsernameLabel.fill = rgb(170, 150, 130)
                signInUsernameLabel.size = 15
                signInUsernameLabel.value = 'username'

    if app.isEditingSignUpPassword:
        invalidKeys = ['up', 'down', 'left', 'right', 'tab', 'escape']
        if key == 'backspace':
            currentSignInPasswordValue = signInPasswordLabel.value[:-2]
            signInPasswordLabel.value = f'{currentSignInPasswordValue}_'
        elif key == 'enter':
            app.justExitedSignUpEditingMode = True
            currentSignInPasswordValue = signInPasswordLabel.value[:-1]
            signInPasswordLabel.value = currentSignInPasswordValue
            app.isEditingSignUpPassword = False
            app.isSigningIn = True
            if signInPasswordLabel.value == 'password' or signInPasswordLabel.value == '':
                signInPasswordLabel.fill = rgb(170, 150, 130)
                signInPasswordLabel.size = 15
                signInPasswordLabel.value = 'password'
        elif key == 'space':
            currentSignInPasswordValue = signInPasswordLabel.value[:-1]
            signInPasswordLabel.value = f'{currentSignInPasswordValue} _'
        elif signInPasswordLabel.width < 190 and not(key in invalidKeys):
            currentSignInPasswordValue = signInPasswordLabel.value[:-1]
            signInPasswordLabel.value = f'{currentSignInPasswordValue}{key}_'
        if key == 'escape':
            app.justExitedSignUpEditingMode = True
            currentSignInPasswordValue = signInPasswordLabel.value[:-1]
            signInPasswordLabel.value = currentSignInPasswordValue
            app.isEditingSignUpPassword = False
            app.isSigningIn = True
            if signInPasswordLabel.value == 'password' or signInPasswordLabel.value == '':
                signInPasswordLabel.fill = rgb(170, 150, 130)
                signInPasswordLabel.size = 15
                signInPasswordLabel.value = 'password'

    if app.isSigningIn:
        if (key == 'down' or key == 's') and signInOptionSelector.position != 3:
            signInOptionSelector.centerY += 70
            signInOptionSelector.position += 1
        if (key == 'up' or key == 'w') and signInOptionSelector.position != 1:
            signInOptionSelector.centerY -= 70
            signInOptionSelector.position -= 1
        if key == 'escape':
            app.isSigningIn = False
            app.inMainMenu = True
            mainMenu.visible = True
            signInScreen.visible = False
            mainMenu.toFront()
        if key == 'enter':
            if signInOptionSelector.position == 1 and not(app.justExitedSignUpEditingMode):
                signInUsernameLabel.value = '_'
                app.isEditingSignUpUsername = True
                app.isSigningIn = False
                signInUsernameLabel.fill = rgb(142, 121, 102)
                signInUsernameLabel.size = 18
            elif signInOptionSelector.position == 2 and not(app.justExitedSignUpEditingMode):
                signInPasswordLabel.value = '_'
                app.isEditingSignUpPassword = True
                app.isSigningIn = False
                signInPasswordLabel.fill = rgb(142, 121, 102)
                signInPasswordLabel.size = 18
            elif signInOptionSelector.position == 3 and (((signInUsernameLabel.value != 'username') and (signInPasswordLabel.value != 'password'))):
                app.submittedCredentials = True
                app.isSigningIn = False
            elif app.justExitedSignUpEditingMode:
                app.justExitedSignUpEditingMode = False

    if app.isShowingLoginResult:
        if key:
            signInScreenResultOutputGroup1.visible = False
            signInScreenResultOutputGroup2.visible = False
            signInScreenResultOutputGroup3.visible = False
            app.inMainMenu = True
            mainMenu.visible = True
            mainMenu.toFront()
            app.inClassicGame = False
            app.inSpeedRunGame = False
            app.editingUsername = False
            app.justExitedEditingMode = False
            app.isSigningIn = False
            signInScreen.visible = False
            app.isEditingSignUpUsername = False
            app.isEditingSignUpPassword = False
            app.submittedCredentials = False
            app.justExitedSignUpEditingMode = False
            app.isShowingLoginResult = False
    
    if app.inSpeedRunGame:
        if not(app.hasStartedSpeedRunning) and (key in ['up', 'down', 'right', 'left', 'w', 'a', 's', 'd']) and not(app.gridIsFull):
            app.speedRunStartTime = time.time()
            app.hasStartedSpeedRunning = True
        if key == 'r':
            resetGameSpeedRun(usernameLabel.value)
            return
        result = checkGameOverSpeedRun()
        if result != 'continue':
            showGameOverScreenSpeedRun(result)
            app.hasStartedSpeedRunning = False
            return
        moved = False
        if key == 'up' or key == 'w':
            moved = moveUpSpeedRun()
        if key == 'down' or key == 's':
            moved = moveDownSpeedRun()
        if key == 'left' or key == 'a':
            moved = moveLeftSpeedRun()
        if key == 'right' or key == 'd':
            moved = moveRightSpeedRun()
        if moved:
            addRandomTileSpeedRun()
        drawTilesSpeedRun()
        result = checkGameOverSpeedRun()
        if result != 'continue':
            showGameOverScreenSpeedRun(result)
            app.hasStartedSpeedRunning = False
        if key == 'escape':
            app.inSpeedRunGame = False
            app.inMainMenu = True
            changeSpeedRunGameVisibility(False)
            mainMenu.toFront()
            mainMenu.visible = True


    if app.submittedCredentials:
        signInResult = handle_authentication(signInUsernameLabel.value, signInPasswordLabel.value)
        if signInResult == 1:
            signInScreenResultOutputGroup1Username.value = signInUsernameLabel.value
            signInScreenResultOutputGroup1.visible = True
            signInScreenResultOutputGroup1.toFront()
            usernameLabel.value = signInUsernameLabel.value
            app.isLoggedIn = True
            resetGame()
            highScore.value = read_high_scores()[usernameLabel.value]
            mainMenuHighScoreLabel.value = read_high_scores()[usernameLabel.value]
            highScoreTrophy.right = mainMenuHighScoreLabel.left - 10
        elif signInResult == 2:
            signInScreenResultOutputGroup2Username.value = signInUsernameLabel.value
            signInScreenResultOutputGroup2.visible = True
            signInScreenResultOutputGroup2.toFront()
            app.isLoggedIn = False
        else:
            signInScreenResultOutputGroup3Username.value = signInUsernameLabel.value
            signInScreenResultOutputGroup3.visible = True
            signInScreenResultOutputGroup3.toFront()
            usernameLabel.value = signInUsernameLabel.value
            usernameLabel.value = signInUsernameLabel.value
            app.isLoggedIn = True
            resetGame()
            highScore.value = read_high_scores()[usernameLabel.value]
            mainMenuHighScoreLabel.value = read_high_scores()[usernameLabel.value]
            highScoreTrophy.right = mainMenuHighScoreLabel.left - 10
        app.isShowingLoginResult = True


    if app.inMainMenu:
        if (key == 'down' or key == 's') and selector.position != 4:
            selector.centerY += 70
            selector.position += 1
        if (key == 'up' or key == 'w') and selector.position != 2:
            selector.centerY -= 70
            selector.position -= 1
        if key == 'enter':
            if selector.position == 2 and app.isLoggedIn:
                app.inMainMenu = False
                mainMenu.visible = False
                app.inClassicGame = True
            elif selector.position == 3 and app.isLoggedIn:
                app.inMainMenu = False
                app.inSpeedRunGame = True
                changeSpeedRunGameVisibility(True)
            elif selector.position == 4 and not(app.isLoggedIn):
                app.isSigningIn = True
                app.inMainMenu = False
                signInScreen.visible = True
                signInScreen.toFront()
        if key == 'i':
            app.inMainMenu = False
            app.isShowingInstructions = True

    if app.isShowingInstructions:
        if key == 'left' and app.currentPage > 0:
            app.currentPage -= 1
        if key == 'right' and app.currentPage < len(pages) - 1:
            app.currentPage += 1
        drawPage()
        if key == 'escape':
            app.isShowingInstructions = False
            app.inMainMenu = True
            mainMenu.visible = True
            app.currentLabels.clear()
            mainMenu.toFront()
    if app.isShowingSpeedRunLeaderboard:
        if key == 'escape':
            app.isShowingSpeedRunLeaderboard = False
            changeSpeedRunGameVisibility(True)
            app.speedRunLeaderboard.clear()
            app.inSpeedRunGame = True

def onMousePress(mouseX, mouseY):
    if app.inClassicGame:
        if resetButton.hits(mouseX, mouseY) or (tryAgainButton.hits(mouseX, mouseY) and tryAgainButton.visible):
            resetGame()
    if app.inMainMenu:
        if classicGameButton.hits(mouseX, mouseY) and app.isLoggedIn:
            app.inMainMenu = False
            mainMenu.visible = False
            app.inClassicGame = True
            selector.centerY = 220
        if signInButton.hits(mouseX, mouseY) and not(app.isLoggedIn):
            app.isSigningIn = True
            app.inMainMenu = False
            selector.centerY = 360
            signInScreen.visible = True
            signInScreen.toFront()
        if speedunButton.hits(mouseX, mouseY) and app.isLoggedIn:
            app.inMainMenu = False
            app.inSpeedRunGame = True
            selector.centerY = 290
            changeSpeedRunGameVisibility(True)
        if trophy.hits(mouseX, mouseY):
            app.isShowingLeaderboard = True
            app.inMainMenu = False
            app.leaderboard = createLeaderboard()
    if app.inSpeedRunGame:
        if speedRunTryAgainButton.hits(mouseX, mouseY) and speedRunTryAgainButton.visible:
            resetGameSpeedRun(usernameLabel.value)
        if speedRunRestartButton.hits(mouseX, mouseY):
            resetGameSpeedRun(usernameLabel.value)
        if speedRunShowSpeedRunTimes.hits(mouseX, mouseY):
            app.inSpeedRunGame = False
            app.isShowingSpeedRunLeaderboard = True
            changeSpeedRunGameVisibility(False)
            app.speedRunLeaderboard = createSpeedRunLeaderboard(usernameLabel.value)
        if speedRunReturnToMenu.hits(mouseX, mouseY):
            app.inSpeedRunGame = False
            app.inMainMenu = True
            changeSpeedRunGameVisibility(False)
            mainMenu.toFront()
            mainMenu.visible = True

def onStep():
    if app.inSpeedRunGame:
        if app.hasStartedSpeedRunning and not(app.gridIsFull):
            elapsed_time = time.time() - app.speedRunStartTime
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            milliseconds = int((elapsed_time % 1) * 1000)
            timeOutput = f'{minutes:02}:{seconds:02}.{milliseconds:03}'
            speedRunTimeLabel.value = timeOutput
            result = checkForValueInGrid()
            if result:
                app.newTime.append(timeOutput)
                if speedRunTimeLabel1.value == '-':
                    speedRunTimeLabel1.value = timeOutput
                elif speedRunTimeLabel2.value != '-':
                    speedRunTimeLabel1.value == speedRunTimeLabel2.value
                    speedRunTimeLabel2.value = timeOutput
                    speedRunLabel1.value *= 2
                    speedRunLabel2.value *= 2
                    speedRunLabel3.value *= 2
                    speedRunTimeTrackerTileBG1.clear()
                    speedRunTimeTrackerTileBG1.add(
                        Rect(40, 40, 30, 25, fill = getTileColourSpeedRun(speedRunLabel1.value), align = 'center'),
                        speedRunCreateSideSmoothCorners(30, 40, 40, rgb(250, 248, 239), getTileColourSpeedRun(speedRunLabel1.value), 25, 'l')
                    )
                    speedRunTimeTrackerTileBG2.clear()
                    speedRunTimeTrackerTileBG2.add(
                        Rect(40, 70, 30, 25, fill = getTileColourSpeedRun(speedRunLabel2.value), align = 'center'),
                        speedRunCreateSideSmoothCorners(30, 40, 70, rgb(250, 248, 239), getTileColourSpeedRun(speedRunLabel2.value), 25, 'l')
                    )
                    speedRunTimeTrackerTileBG3.clear()
                    speedRunTimeTrackerTileBG3.add(
                        Rect(40, 100, 30, 25, fill = getTileColourSpeedRun(speedRunLabel3.value), align = 'center'),
                        speedRunCreateSideSmoothCorners(30, 40, 100, rgb(250, 248, 239), getTileColourSpeedRun(speedRunLabel3.value), 25, 'l')
                    )
                    speedRunTimeTrackerTileBG1.centerY -= 6
                    speedRunTimeTrackerTileBG1.centerX += 5
                    speedRunTimeTrackerTileBG2.centerY -= 6
                    speedRunTimeTrackerTileBG2.centerX += 5
                    speedRunTimeTrackerTileBG3.centerY -= 6
                    speedRunTimeTrackerTileBG3.centerX += 5
                    speedRunLabels.toFront()
                else:
                    speedRunTimeLabel2.value = timeOutput

mainMenu.toFront()
drawPage()
app.currentLabels.toFront()
resetGame()
resetGameSpeedRun(usernameLabel.value)

cmu_graphics.run()