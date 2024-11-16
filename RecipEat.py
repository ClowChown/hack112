
#modifed version of code in this blog: (https://medium.com/@your_data_scientist_bestie/exploring-pythons-delicious-side-spoonacular-api-adventures-34af451262bc)
#also used modified code from this blog: (https://georginaquach.wordpress.com/2020/03/26/example-post-2/)
#also used some chatgpt to debug, but reformated by Theresa and Dora
#had help from Varun as well (bc we won speed cts!)

import requests
import json

# common code block
from cmu_graphics import *

# classes
class Food:
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        foodType = self.getType()
        return f'{foodType}("{self.name}")'

    def getName(self):
        return self.name

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return isinstance(other, Food) and (self.name == other.name)
    
    def getType(self):
        foodTypeRaw = str(type(self))
        foodType = foodTypeRaw[foodTypeRaw.find('.')+1:-2]
        return foodType

class Fruit(Food):
    def __init__(self, name):
        super().__init__(name)
        self.quantity = 0
    
    def addQuantity(self, quantity):
        self.quantity += quantity
    
    def getQuantity(self):
        return self.quantity

class Grain(Food):
    def __init__(self, name):
        super().__init__(name)
        self.weight = 0
    
    def addWeight(self, weight):
        self.weight += weight
    
    def getWeight(self):
        return self.weight

class Vegetable(Food):
    def __init__(self, name):
        super().__init__(name)
        self.quantity = 0
    
    def addQuantity(self, quantity):
        self.quantity += quantity
    
    def getQuantity(self):
        return self.quantity
    
class Dairy(Food):
    def __init__(self, name):
        super().__init__(name)
        self.cup = 0
    
    def addCup(self, cup):
        self.cup += cup
    
    def getCup(self):
        return self.cup

class Protein(Food):
    def __init__(self, name):
        super().__init__(name)


# animations (interface)
def onAppStart(app):
    # app background setup
    app.width = 600
    app.height = 600
    app.search = False
    
    #shopping list
    app.shoppingListWidth = app.width//4
    app.shoppingListColor = 'plum'
    app.ingredients = set()
    app.latestIngredients = []
    
    #food filter buttons
    app.foodFiltersTop = 0
    app.foodFiltersLeft = app.shoppingListWidth
    app.foodFiltersNumber = 5
    app.foodFiltersWidth = (app.width-app.shoppingListWidth)/app.foodFiltersNumber
    app.foodFiltersHeight = app.height/16
    app.foodFiltersBorderWidth = 2
    app.foodFiltersLabels = ["Dairy", "Fruits", "Grains", "Proteins", "Vegetables"]
    app.foodFiltersFontSize = app.foodFiltersWidth*0.125
    # filter active
    app.dairy = True
    app.fruits = False
    app.grains = False
    app.proteins = False
    app.vegetables = False

    #ingredient lists
    app.proteinList = [[Protein("chicken"), Protein("beef"), Protein("pork"), Protein("egg")], [Protein("tofu"), Protein("salmon"), Protein("tuna"), Protein("shrimp")], [Protein("lamb"), Protein("turkey"), Protein("bacon"), Protein("cod")], [Protein("mackerel"), Protein("duck"), Protein("lentils"), Protein("black beans")], [Protein("chickpeas"), Protein("edamame"), Protein("almonds"), Protein("peanuts")]]
    app.grainList = [[Grain("bread"), Grain("white rice"),Grain("brown rice"), Grain("wheat")], [Grain("corn"), Grain("barley"), Grain("flour"), Grain("oats")], [Grain("rice cake"), Grain("bagel"), Grain("pasta"), Grain("quinoa")], [Grain("millet"), Grain("buckwheat"), Grain("teff"), Grain("almond flour")], [Grain("corn flour"), Grain("cornstarch"), Grain("cornmeal"), Grain("wild rice")]]
    app.vegetableList = [[Vegetable("potato"), Vegetable("onion"), Vegetable("carrot"), Vegetable("tomato")], [Vegetable("garlic"), Vegetable("spinach"), Vegetable("cucumber"), Vegetable("broccoli")], [Vegetable("cauliflower"), Vegetable("bell pepper"), Vegetable("mushroom"), Vegetable("zucchini")], [Vegetable("sweet potato"), Vegetable("green bean"), Vegetable("lettuce"), Vegetable("pea")], [Vegetable("cabbage"), Vegetable("celery"), Vegetable("corn"), Vegetable("asparagus")]]
    app.fruitList = [[Fruit("apple"), Fruit("banana"), Fruit("blackberry"), Fruit("blueberry")], [Fruit("cherry"), Fruit("coconut"), Fruit("cranberry"), Fruit("grape")], [Fruit("grapefruit"),Fruit("lemon"), Fruit("mango"), Fruit("melon")], [Fruit("orange"), Fruit("papaya"), Fruit("peach"), Fruit("pear")], [Fruit("pineapple"), Fruit("pomegranate"), Fruit("raspberry"), Fruit("strawberry")]]
    app.dairyList = [[Dairy('milk'), Dairy('oat milk'), Dairy('soy milk'), Dairy('almond milk')], [Dairy('yogurt'), Dairy('cream cheese'), Dairy('sourcream'),Dairy('cheese')], [Dairy('whey protein'), Dairy('ice cream'),Dairy('gelato'), Dairy('cream')], [Dairy('butter'), Dairy('condensed milk'), Dairy('ghee'), Dairy('half and half')], [Dairy('coffee'),Dairy('tea'), Dairy('panna cotta'), Dairy('cottage cheese')]]
 
    #food grid
    app.foodGridRows = 10
    app.foodGridCols = 9
    app.board = app.dairyList
    app.foodGridTop = app.foodFiltersTop + (app.foodFiltersHeight * 2)
    app.foodGridLeft = app.shoppingListWidth
    app.foodGridRight = 0
    app.foodGridWidth = (app.width-app.shoppingListWidth)/(app.foodGridCols)
    app.foodGridHeight = (app.height-app.foodGridTop) / (app.foodGridRows)

    #food quantity popup
    app.popUpWidth = (app.width - app.shoppingListWidth)*3/5
    app.popUpHeight = app.height // 3
    app.popUpLeft = (app.width+app.shoppingListWidth)//2 - app.popUpWidth//2
    app.popUpTop = app.height//2 - app.popUpHeight//2
    
    app.escapeLineX =  (app.popUpWidth * (19/20)) + app.popUpLeft
    app.escapeLineY = app.popUpHeight//10 + app.popUpTop
    app.escapeLineLength = app.popUpWidth//13
    
    app.popUpActivated = False

    # search button
    app.searchWidth = app.shoppingListWidth // 2
    app.searchHeight = app.searchWidth // 2
    app.searchTop = app.foodGridTop + ((app.foodGridRows-1) * app.foodGridHeight)
    app.searchLeft = app.shoppingListWidth//2 - app.searchWidth//2
    app.searchFontSize = app.searchWidth * 0.15

    # search screen
    app.searchScreenWidth = app.width//2
    app.searchScreenHeight = app.height//2
    app.searchScreenTop = app.width//2 - app.searchScreenWidth//2
    app.searchScreenLeft = app.height//2 - app.searchScreenHeight//2
    # filters
    app.intolerances = ['Dairy', 'Egg', 'Gluten','Peanut', 'Sesame', 'Shellfish', 'Soy',  'Tree Nut']
    app.intolerances2 = ['Sesame', 'Shellfish', 'Soy',  'Tree Nut']
    app.intolerancesWidth, app.intolerancesHeight = (app.width//2)//(len(app.intolerances)//2), app.height//16
    app.intolerancesLeft, app.intolerancesTop = app.width//4, app.searchScreenTop+app.searchScreenTop//3
    app.intolerancesTop2 = app.searchScreenTop+app.searchScreenTop//3 + app.intolerancesHeight
    
    app.cuisines=['American', 'Chinese', 'Indian', 'Italian', 'Japanese', 'Mexican', 'Middle Eastern','Thai']
    app.cuisines2 = ['Japanese', 'Mexican','Thai']
    app.cuisineWidth, app.cuisineHeight = (app.width//2)//(len(app.cuisines)//2), app.height//16
    app.cuisineLeft, app.cuisineTop = app.width//4, app.searchScreenTop+app.searchScreenTop//3 + (app.cuisineHeight*3)
    app.cuisineTop2 = app.searchScreenTop+app.searchScreenTop//3 + (app.cuisineHeight *4)

    # start button
    app.startWidth, app.startHeight = app.searchScreenWidth//2, app.searchScreenWidth//8
    app.startLeft = app.searchScreenLeft + app.startWidth//2
    app.startTop = app.searchScreenTop + (app.startHeight * 7)

    app.recipeReturned = False
    app.recipe = None

def redrawAll(app):
    drawPantry(app)
    drawFoods(app)
    drawFoodFilters(app)
    drawSearchButton(app)
    if app.popUpActivated:
         drawPopUp(app)
    if app.search == True:
        drawSearchScreen(app)
    if app.recipeReturned:
        drawRecipe(app)

# drawing functions
def drawRecipe(app):
    drawRect(app.width / 2 - 200, app.height / 2 - 200, 400, 400, fill='white')
    recipename = str(app.recipe)
    length = len(recipename)
    splits = int(length // 6)
    recipe1 = recipename[:splits]
    recipe2 = recipename[splits:splits*2]
    recipe3 = recipename[splits*2:splits*3]
    recipe4 = recipename[splits*3:splits*4]
    recipe5 = recipename[splits*4:splits*5]
    recipe6 = recipename[splits*5:]

    drawLabel(recipe1, app.width / 2, app.height / 2 - 60)
    drawLabel(recipe2, app.width / 2, app.height / 2 - 30)
    drawLabel(recipe3, app.width / 2, app.height / 2)
    drawLabel(recipe4, app.width / 2, app.height / 2 + 30)
    drawLabel(recipe5, app.width / 2, app.height / 2 + 60)
    drawLabel(recipe6, app.width / 2, app.height / 2 + 90)

def drawIntolerances(app):
    for i in range(len(app.intolerances)//2):
        drawRect(app.intolerancesLeft+(app.intolerancesWidth * i), app.intolerancesTop, app.intolerancesWidth, app.intolerancesHeight, fill='pink', border='black', borderWidth=2)
        drawLabel(app.intolerances[i], app.intolerancesLeft +app.intolerancesWidth//2 + (app.intolerancesWidth * i), app.intolerancesTop+app.intolerancesHeight//2, align='center', size=app.intolerancesWidth*0.2,)
    for i in range(len(app.intolerances2)):
            drawRect(app.intolerancesLeft + (app.intolerancesWidth * i), app.intolerancesTop2, app.intolerancesWidth, app.intolerancesHeight, fill='pink', borderWidth=2, border='black')
            drawLabel(app.intolerances2[i], app.intolerancesLeft+app.intolerancesWidth//2 +(app.intolerancesWidth * i), app.intolerancesTop2+app.intolerancesHeight//2, align='center', size=app.intolerancesWidth*0.2)

def drawCuisines(app):
    for i in range(len(app.cuisines)//2):
        drawRect(app.cuisineLeft + (app.cuisineWidth * i), app.cuisineTop, app.cuisineWidth, app.cuisineHeight, fill='pink', borderWidth=2, border='black')
        drawLabel(app.cuisines[i], app.cuisineLeft+(i * app.cuisineWidth)+app.cuisineWidth//2, app.cuisineTop+app.cuisineHeight//2, align='center', size=app.cuisineWidth*0.2)

    for i in range(len(app.cuisines2)):
        drawRect(app.cuisineLeft + (app.cuisineWidth * i), app.cuisineTop2, app.cuisineWidth, app.cuisineHeight, fill='pink', borderWidth=2, border='black')
        drawLabel(app.cuisines2[i], app.cuisineLeft+(i * app.cuisineWidth)+app.cuisineWidth//2, app.cuisineTop2+app.cuisineHeight//2, align='center', size=app.cuisineWidth*0.2)


def drawSearchScreen(app):
    #when pop-up shows appears, makes the background darker
    drawRect(app.shoppingListWidth, 0, app.width-app.shoppingListWidth, app.height, fill='black', opacity=35)
    drawRect(app.searchScreenLeft, app.searchScreenTop, app.searchScreenWidth, 
             app.searchScreenHeight, fill='pink', border='black', borderWidth=app.foodFiltersBorderWidth*2)
    drawExit(app)
    drawIntolerances(app)
    drawCuisines(app)
    drawStartButton(app)

def drawSearchButton(app):
    drawRect(app.searchLeft, app.searchTop, app.searchWidth, app.searchHeight, fill='pink', 
             border='black', borderWidth=app.foodFiltersBorderWidth*2)
    drawLabel('SEARCH', app.searchLeft + app.searchWidth//2, app.searchTop + app.searchHeight//2, 
              size=app.searchFontSize, bold=True, align='center')
    
def drawStartButton(app):
    drawRect(app.startLeft, app.startTop, app.startWidth, app.startHeight, fill='pink', border='black', borderWidth=2)
    drawLabel('SEARCH', app.startLeft + app.startWidth//2, app.startTop + app.startHeight//2, align='center', size=app.startWidth*0.2)


def drawExit(app):
    x0 = app.searchScreenLeft + (app.searchScreenWidth * 14/16)
    y0 = app.searchScreenTop + (app.searchScreenHeight * 2/16)
    x1 = app.searchScreenLeft + (app.searchScreenWidth * 15/16)
    y1 = app.searchScreenTop + (app.searchScreenHeight * 1/16)
    x2 = app.searchScreenLeft + (app.searchScreenWidth * 15/16)
    y2 = app.searchScreenTop + (app.searchScreenHeight * 2/16)
    x3 = app.searchScreenLeft + (app.searchScreenWidth * 14/16)
    y3 = app.searchScreenTop + (app.searchScreenHeight * 1/16)
    drawLine(x0, y0, x1, y1, fill='red')
    drawLine(x2, y2, x3, y3, fill='red')


def drawPantry(app):
    drawRect(0, 0, app.shoppingListWidth, app.height, fill=app.shoppingListColor)
    drawLabel('Pantry', app.shoppingListWidth//2, app.height//30, size=(app.shoppingListWidth* 0.15), bold=True)
    
    for i in range(len(app.ingredients)):
        drawLabel(list(app.ingredients)[i].name, app.shoppingListWidth//2, (app.height//30)*3+i*(app.height//30), bold=True, fill='white', size=18)
    
def drawFoods(app):
    x = app.foodGridLeft
    y = app.foodGridTop
    for i in range(app.foodGridRows):
        for j in range(app.foodGridCols):
            if i % 2 == 0 and j % 2 == 1:
                cellLeft, cellTop = x + (j * app.foodGridWidth), y + (i * app.foodGridHeight)
                drawCell(app, cellLeft, cellTop)

def drawCell(app, left, top):
    drawRect(left, top, app.foodGridWidth, app.foodGridHeight)
    ingredient = isIngredient(app, left + 1, top + 1)
    drawLabel(ingredient.name, left + app.foodGridWidth / 2,
              top + app.foodGridHeight / 2, fill='white')

def drawFoodFilters(app):
    for i in range(app.foodFiltersNumber):
        foodFiltersLeft = app.foodFiltersLeft + app.foodFiltersWidth*i
        if app.dairy:
            highlight = 'Dairy'
        elif app.fruits:
            highlight = 'Fruits'
        elif app.grains:
            highlight = 'Grains'
        elif app.proteins:
            highlight = 'Proteins'
        elif app.vegetables:
            highlight = 'Vegetables'
        if app.foodFiltersLabels[i] == highlight:
            color = 'purple'
        else:
            color = 'pink'
        drawRect(foodFiltersLeft, app.foodFiltersTop, app.foodFiltersWidth, app.foodFiltersHeight, fill=color, border='black', borderWidth = app.foodFiltersBorderWidth)
        drawLabel(app.foodFiltersLabels[i], foodFiltersLeft + app.foodFiltersWidth//2, (app.foodFiltersTop+app.foodFiltersHeight)//2, bold=True, size=app.foodFiltersFontSize)
    	
      #draws another layer of the border to re-justify the  size
        drawRect(app.foodFiltersLeft, app.foodFiltersTop, app.width-app.shoppingListWidth, app.foodFiltersHeight, fill=None, border='black', borderWidth = 2*app.foodFiltersBorderWidth)
    	
      #draws another layer of the border to re-justify the  size
        drawRect(app.foodFiltersLeft, app.foodFiltersTop, app.width-app.shoppingListWidth, app.foodFiltersHeight, fill=None, border='black', borderWidth = 2*app.foodFiltersBorderWidth)

def drawPopUp(app):
    #when pop-up appears, makes the background darker
    drawRect(app.shoppingListWidth, 0, app.width-app.shoppingListWidth, app.height, fill='black', opacity=35)
    
    drawRect(app.popUpLeft, app.popUpTop, app.popUpWidth, app.popUpHeight, fill='white')
    
    #escape button
    drawLine(app.escapeLineX, app.escapeLineLength//2 + app.escapeLineY, app.escapeLineX, app.escapeLineY - app.escapeLineLength//2, fill='red', rotateAngle = 45, lineWidth = 3)
    drawLine(app.escapeLineX-app.escapeLineLength//2, app.escapeLineY, app.escapeLineX+app.escapeLineLength//2, app.escapeLineY, fill='red', rotateAngle = 45, lineWidth = 3)
    
    #add to pantry button
    pantryButtonWidth = app.popUpWidth//3
    pantryButtonHeight = app.popUpHeight//8
    pantryButtonLeft = app.popUpLeft+app.popUpWidth//2-pantryButtonWidth//2
    pantryButtonTop = app.popUpTop + app.popUpHeight*(5/6)-pantryButtonHeight//2
    
    drawRect(pantryButtonLeft, pantryButtonTop, pantryButtonWidth, pantryButtonHeight)
    drawLabel('Add to Pantry', pantryButtonLeft+pantryButtonWidth//2, pantryButtonTop + pantryButtonHeight//2, fill='white', bold=True)
    
    message = "Add " + str(app.latestIngredients[-1].name) + " to pantry?"
    drawLabel(message, app.popUpWidth//2 + app.popUpLeft, app.popUpHeight//2 + app.popUpTop, size=20)

def onMousePress(app, mouseX, mouseY):
    if app.popUpActivated == False:
        getButton(app, mouseX, mouseY)

    #exits the pop-up when the mouse clicks the X button
    if distance(app.escapeLineX, app.escapeLineY, mouseX, mouseY) < app.escapeLineLength//(2.2):
        app.popUpActivated = False
    
    if app.popUpActivated == True:
        pantryButtonWidth = app.popUpWidth//3
        pantryButtonHeight = app.popUpHeight//8
        pantryButtonLeft = app.popUpLeft+app.popUpWidth//2-pantryButtonWidth//2
        pantryButtonTop = app.popUpTop + app.popUpHeight*(5/6)-pantryButtonHeight//2
        latestIngredient = app.latestIngredients[-1]
        if (mouseX > pantryButtonLeft) and (mouseX < pantryButtonWidth + pantryButtonLeft) and (mouseY > pantryButtonTop) and (mouseY < pantryButtonTop+pantryButtonHeight):
            app.popUpActivated = False
            app.ingredients.add(latestIngredient)
    changeBoard(app)

def getButton(app, mouseX, mouseY):
    if app.search != True:
        ingredient = isIngredient(app, mouseX, mouseY)
        print(ingredient)
        if ingredient != None:
            app.popUpActivated = True
            app.latestIngredients.append(ingredient)
        foodFilter = isFilter(app, mouseX, mouseY)
        if foodFilter != None:
            app.dairy = app.fruits = app.grains = app.proteins = app.vegetables = False
            if foodFilter == 'dairy': app.dairy = True
            if foodFilter == "fruits": app.fruits = True
            if foodFilter == 'grains': app.grains = True
            if foodFilter == 'proteins': app.proteins = True
            if foodFilter == 'vegetables': app.vegetables = True
            return
    if isSearch(app, mouseX, mouseY):
        app.search = True
        app.cuisinesFiltered = set()
        app.intolerancesFiltered = set()
        return
    if getCuisine(app, mouseX, mouseY) != None and app.search==True:
        if getCuisine(app, mouseX, mouseY) in app.cuisinesFiltered: app.cuisinesFiltered.remove(getCuisine(app, mouseX, mouseY))
        app.cuisinesFiltered.add(getCuisine(app, mouseX, mouseY))
        print(app.cuisinesFiltered)
    
    if getIntolerance(app, mouseX, mouseY) != None and app.search == True:
        if getIntolerance(app, mouseX, mouseY) in app.intolerancesFiltered: app.intolerancesFiltered.remove(getIntolerance(app, mouseX, mouseY))
        app.intolerancesFiltered.add(getIntolerance(app, mouseX, mouseY))
        print(app.intolerancesFiltered)
    
    if isStart(app, mouseX, mouseY) != None and app.search == True:
        app.recipe = getRecipes(app)
        app.recipeReturned = True

    if isExit(app, mouseX, mouseY) and app.search == True:
        app.search = False

def isStart(app, x, y):
    if (x > app.startLeft and x < app.startLeft + app.startWidth and
        y > app.startTop and y < app.startTop + app.startHeight):
        return True
    return None

def getIntolerance(app, x, y):
    if (x < app.intolerancesLeft or x > app.intolerancesLeft + (app.intolerancesWidth * (len(app.intolerances)//2)) or
        y < app.intolerancesTop or y > app.intolerancesTop + (app.intolerancesHeight*2)):
        return None
    else:
        if app.intolerancesTop < y < app.intolerancesTop2:
            newCol = ((x- app.intolerancesLeft)//(app.intolerancesWidth))
            return app.intolerances[newCol]
        else:
            if app.intolerancesLeft < x < app.intolerancesLeft * (app.intolerancesWidth * len(app.intolerances2)):
                newCol = ((x- app.intolerancesLeft)//(app.intolerancesWidth))
                return app.intolerances2[newCol]

def getCuisine(app, x, y):
    if (x < app.cuisineLeft or x > app.cuisineLeft + (app.cuisineWidth * (len(app.cuisines)//2)) or
        y < app.cuisineTop or y > app.cuisineTop + (app.cuisineHeight*2)):
        return None
    else:
        if app.cuisineTop < y < app.cuisineTop2:
            newCol = ((x- app.cuisineLeft)//(app.cuisineWidth))
            return app.cuisines[newCol]
        else:
            if app.cuisineLeft < x < app.cuisineLeft * (app.cuisineWidth * len(app.cuisines2)):
                newCol = ((x- app.cuisineLeft)//(app.cuisineWidth))
                return app.cuisines2[newCol]

def changeBoard(app):
    if app.dairy:
        app.board = app.dairyList
    elif app.fruits:
        app.board = app.fruitList
    elif app.grains:
        app.board = app.grainList
    elif app.vegetables:
        app.board = app.vegetableList
    else:
        app.board = app.proteinList

# def boardColReformatVal(n):
#     if n == '1':
#         result = -1
#     elif n == '3':
#         result = -2
#     elif n == '5':
#         result = -3
#     else:
#         result = -4
#     return result
    
def isIngredient(app, mouseX, mouseY):
    if (mouseX < app.foodGridLeft or mouseX > app.width or
        mouseY < app.foodGridTop or mouseY > app.height):
        return None
    else:
        newRow = (mouseY - app.foodGridTop) // app.foodGridHeight
        newCol = (mouseX - app.foodGridLeft) // app.foodGridWidth

        if newRow % 2 == 0:
            row = int(newRow // 2)
        else:
            return None
        
        if newCol % 2 == 1:
            col = int(newCol // 2)
        else:
            return None

        return app.board[row][col]

def isFilter(app, x, y):
    if (x < app.foodFiltersLeft or x > app.width or
        y < 0 or y > app.foodFiltersHeight):
        return None
    else:
        newCol = (x - app.foodFiltersLeft) // app.foodFiltersWidth
        filterIndexes = ["dairy", "fruits", "grains", "proteins", "vegetables"]
        return filterIndexes[int(newCol)]
def isExit(app, x, y):
    x0 = app.searchScreenLeft + (app.searchScreenWidth * 14/16)
    y0 = app.searchScreenTop + (app.searchScreenHeight * 2/16)
    x1 = app.searchScreenLeft + (app.searchScreenWidth * 15/16)
    y1 = app.searchScreenTop + (app.searchScreenHeight * 1/16)
    app.exitLeft, app.exitTop, app.exitWidth, app.exitHeight = x0, y1, x1-x0, y0-y1
    if (x > app.exitLeft and x < app.exitLeft + app.exitWidth and
        y > app.exitTop and y < app.exitTop + app.exitHeight):
        return True
    return False

def isSearch(app, x, y):
    if not (x < app.searchLeft or x > app.searchLeft+app.searchWidth or
        y < app.searchTop or y > app.searchTop + app.searchHeight):
        return True
    return False
        
def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**(0.5)

def getRecipes(app):
    recipes = callRecipe(app.ingredients, app.intolerancesFiltered, app.cuisinesFiltered, set())
    return recipes



def getIngredients(selectedIngredidents):
    query = ''
    for v in selectedIngredidents:
        query += v.name + ',+'
    query = query[0:-2]
    return query 

def getOtherParameters(input):
    if len(input) == 0:
        return None
    else:
        output = ''
        for v in input:
            output += v + ','
        return output[:-1]

class Recipe:
    def __init__(self, name, servings, prepTime, ingredients):
        self.name = name
        self.servings = servings
        self.prepTime = prepTime
        self.ingredients = ingredients
    
    def __repr__(self):
        if self.servings == 1:
            servingMessage = 'serving'
        else:
            servingMessage = 'servings'
        return (f'{self.name}: {self.servings} {servingMessage} and ' +
               f'{self.prepTime} mins of prep time ' 
               f'with ingredients: {self.ingredients}')

class Ingredient:
    def __init__(self, name, metric, amount):
        self.name = name
        self.metric = metric
        self.amount = amount

    def __repr__(self):
        if self.metric == '':
            message = f'{self.amount} {self.name}'
            if self.amount == 1 and message[-1] == 's':
                message[:-1]
            elif self.amount != 1 and message[-1] != 's':
                message += 's'
            return message
        else:
            if self.amount == 1 and self.metric[-1] == 's':
                metric = self.metric[:-1]
            elif self.amount != 1 and self.metric[-1] != 's':
                metric = self.metric + 's'
            else:
                metric = self.metric
            return f'{self.amount} {metric} of {self.name}'

# Query --> a list of arguments passed in by the user via button clicks
def callRecipe(ingredients, intolerances, cuisine, excludeCuisine): 

    ingredients = getIngredients(ingredients)
    intolerances = getOtherParameters(intolerances)
    cuisine = getOtherParameters(cuisine)
    excludeCuisine = getOtherParameters(excludeCuisine)

    apiKey = 'apiKey=1d6527ed7a7c4d099d700dba874020c2'
    api_key = '1d6527ed7a7c4d099d700dba874020c2'

    passList = list()

    includeIngredients = 'includeIngredients=' + ingredients
    passList.append(includeIngredients)
    if intolerances != None:
        intolerances = 'intolerances=' + intolerances
        passList.append(intolerances)
    if cuisine != None:
        cuisine = 'cuisine=' + cuisine
        passList.append(cuisine)
    if excludeCuisine != None:
        excludeCuisine = 'excludeCuisine=' + excludeCuisine
        passList.append(excludeCuisine)
    
    base_url = 'https://api.spoonacular.com/recipes/complexSearch?{}'
    base_url = base_url.format(apiKey)

    for v in passList:
        base_url += '&{}'
        base_url = base_url.format(v)

    ingredients_url = 'https://api.spoonacular.com/recipes/{}/ingredientWidget.json'
    recipe_info_url = 'https://api.spoonacular.com/recipes/{}/information'

    response = requests.get(base_url)
    response.raise_for_status()
    data = response.json()

    # Loop through the recipes
    recipes = data['results']
    for recipe in recipes:
        recipe_id = recipe['id']
        
        # Fetch detailed recipe information (e.g., servings, prep time)
        recipe_info_response = requests.get(recipe_info_url.format(recipe_id), params={'apiKey': api_key})
        recipe_info_response.raise_for_status()
        recipe_info_data = recipe_info_response.json()

        # Print additional information like servings and preparation time
        recipe_name = recipe_info_data['title']
        recipe_servings = recipe_info_data['servings']
        recipe_prep_time = (recipe_info_data['readyInMinutes'], "minutes")

        # Fetch ingredients for the recipe from the ingredientWidget endpoint
        ingredients_response = requests.get(ingredients_url.format(recipe_id), params={'apiKey': api_key})
        ingredients_response.raise_for_status()
        ingredients_data = ingredients_response.json()

        # Print ingredients
        recipe_ingredients = []
        for ingredient in ingredients_data['ingredients']:
            ingredient_to_add = Ingredient(ingredient['name'], ingredient['amount']['us']['unit'], ingredient['amount']['us']['value'])
            recipe_ingredients.append(ingredient_to_add)
        
    final_recipe = Recipe(recipe_name, recipe_servings, recipe_prep_time[0], recipe_ingredients)
    return final_recipe

def main():
    runApp()

main()



