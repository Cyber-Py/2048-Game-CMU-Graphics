from cmu_graphics import *


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

app.background = rgb(142, 121, 102)
app.title = '2048 Game Instructions'

# Instructions divided into sections (pages)
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
        "",
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
        "    Press the 'i' key at any time to bring up these",
        "    instructions again.",
        "",
        "  - 'Escape' Key:",
        "    Press the 'escape' key to go back to the main menu",
        "    or previous screen."
    ]
]

# Current page index
app.currentPage = 0

# List to store the labels on the screen
app.currentLabels = Group()

# Function to draw the current page of instructions
def drawPage():
    
    # Clear previous labels
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
    # Set the initial position for the text
    x, y = 20, 80
    line_height = 20
    
    # Get the current page of instructions
    currentInstructions = pages[app.currentPage]
    
    # Draw each line of the current page
    for line in currentInstructions:
        label = Label(line, x + 3, y, fill=rgb(142, 121, 102), align='left', size=14, bold = True)
        app.currentLabels.add(label)
        y += line_height
    
    # Show page navigation hints
    if app.currentPage > 0:
        prevLabel = Label("< Previous", 60, 40, fill=rgb(142, 121, 102), align='center', size=14, bold = True)
        app.currentLabels.add(prevLabel)
    if app.currentPage < len(pages) - 1:
        nextLabel = Label("Next >", 340, 40, fill=rgb(142, 121, 102), align='center', size=14, bold = True)
        app.currentLabels.add(nextLabel)

# Function to handle key presses for navigation
def onKeyPress(key):
    if key == 'left' and app.currentPage > 0:
        app.currentPage -= 1
    elif key == 'right' and app.currentPage < len(pages) - 1:
        app.currentPage += 1
    # Redraw the page after changing it
    drawPage()

# Draw the first page when the app starts
drawPage()

# Run the app
cmu_graphics.run()
