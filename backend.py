from json import loads, dumps
from os.path import dirname, abspath, join
from os import listdir
from copy import copy

def recursiveDump(foodIn):
        if foodIn.constituents!=[]:
            foodDict=foodIn.__dict__
            dumpList=[]
            for food in foodDict['constituents']:
                foodDump_iter=recursiveDump(food)
                dumpList.append(foodDump_iter)
            foodIn.constituents=dumpList
        foodDump=dumps(foodIn.__dict__)
        foodDump=foodDump.replace('\\','')
        foodDump=foodDump.replace('"{','{')
        foodDump=foodDump.replace('}"','}')
        return foodDump
def recursiveLoad(jsonIn):
    if type(jsonIn)==str:
        jsonDict=loads(jsonIn)
    else:
        jsonDict=jsonIn
    if jsonDict['constituents']!=[]:
        foodList=[]
        for foodEntry in jsonDict['constituents']:
            foodRetrieved=recursiveLoad(foodEntry)
            foodList.append(foodRetrieved)
        # foodOut=foodItem(jsonDict['name'],jsonDict['quantity'],jsonDict['kcal'],jsonDict['protein'],jsonDict['carbs'],jsonDict['fat'],jsonDict['fibers'],constituents=[])
        jsonDict['constituents']=foodList
    #     foodOut=foodItem(jsonDict['name'],jsonDict['quantity'],jsonDict['kcal'],jsonDict['protein'],jsonDict['carbs'],jsonDict['fat'],jsonDict['fibers'],jsonDict['constituents'])        
    # else:
    foodOut=foodItem(jsonDict['name'],jsonDict['quantity'],jsonDict['kcal'],jsonDict['protein'],jsonDict['carbs'],jsonDict['fat'],jsonDict['fibers'],jsonDict['constituents'],jsonDict['notes'])
    return foodOut

class foodHolder:
    def __init__(self,locationToSave=None,filename=str) -> None:
        self.name=filename
        if locationToSave==None:
            self.saveLocation=dirname(abspath(__file__))
        else:
            self.saveLocation=locationToSave
        self.foodList=[]
    def appendFoodFromFile(self,loadFolder,filename):
        if self.name+'.json'==filename: #read file contents and add to foodList
            with open(join(loadFolder,self.name+'.json'),'r') as f:                    
                for row in f:
                    rowDict=loads(row)
                    if rowDict['constituents']!=[]:
                        # rowFood=foodItem(rowDict['name'],rowDict['quantity'],rowDict['kcal'],rowDict['protein'],rowDict['carbs'],rowDict['fat'],rowDict['fibers'],constituents=None)                            
                        # for foodDict in rowDict['constituents']:
                        #     rowFood.constituents.append(foodItem(foodDict['name'],foodDict['quantity'],foodDict['kcal'],foodDict['protein'],foodDict['carbs'],foodDict['fat'],foodDict['fibers'],foodDict['constituents']))                                
                        # self.foodList.append(rowFood)
                        rowFood=recursiveLoad(row)
                        self.foodList.append(rowFood)
                        #läs in constituents separat och skapa foodItems för dem, se till att funkar även med nestade..antagligen rekursiv funktion, kolla om bara behöver rekursiv funktion för att spara, modifiera json-string som får ut från nestade foodItems så tar bort "" mellan nya items i listan...
                    else:
                        self.foodList.append(foodItem(rowDict['name'],rowDict['quantity'],rowDict['kcal'],rowDict['protein'],rowDict['carbs'],rowDict['fat'],rowDict['fibers'],rowDict['constituents'],rowDict['notes']))        
    def addFood(self,food):
        self.foodList.append(food)
    def saveToFile(self):
        with open(join(self.saveLocation,self.name+'.json'),'w') as f:
            for food in self.foodList:
                if food.constituents==[]:
                    f.write(dumps(food.__dict__)+'\n')
                else:
                    dumpStr=recursiveDump(food)
                    f.write(dumpStr+'\n')

class foodItem:
    def __init__(self,name='',quantity=100,kcal=0,protein=0,carbs=0,fat=0,fibers=None,constituents=[],notes='') -> None:
        self.name=name
        self.quantity=quantity
        self.protein=protein
        self.carbs=carbs
        self.fat=fat
        self.fibers=fibers
        self.kcal=kcal
        self.constituents=[]
        self.notes=notes
        if constituents!=[]:
            fiberSum=0
            fiberInfoCounter=0
            self.quantity=0
            for food in constituents:
                self.quantity+=food.quantity
                self.protein+=food.protein
                self.carbs+=food.carbs
                self.fat+=food.fat
                self.kcal+=food.kcal
                # if food.fibers!=None:
                if food.completeFiberInfo:
                    fiberSum+=food.fibers
                    fiberInfoCounter+=1
                self.constituents.append(copy(food))
            if fiberInfoCounter==len(constituents):
                self.completeFiberInfo=True                
            else:
                self.completeFiberInfo=False
            self.fibers=fiberSum
            # self.completeFiberInfo=completeFiberInfo
        else:
            if fibers!=None:
                self.completeFiberInfo=True
            else:
                self.completeFiberInfo=False
    def showNutrients(self):
        print(self.name+', '+str(self.quantity)+'g :',self.kcal,self.protein,self.carbs,self.fat,self.fibers)
    def getFoodData(self):
        return [self.quantity,self.kcal,self.protein,self.carbs,self.fat,self.fibers]
    def showNutrients_constituents(self):
        for constituent in self.constituents:
            constituent.showNutrients()
    def updateNote(self,noteStr):
        self.bote=noteStr
    def changeQuantity(self,newQuantity):
        self.protein=self.protein*newQuantity/self.quantity
        self.carbs=self.carbs*newQuantity/self.quantity
        self.fat=self.fat*newQuantity/self.quantity
        if self.fibers!=None:
            self.fibers=self.fibers*newQuantity/self.quantity
        self.kcal=self.kcal*newQuantity/self.quantity
        for constituent in self.constituents:
            constituent.changeQuantity(newQuantity)
        self.quantity=newQuantity

def sortFoodList(foodListIn,sortBy,reverseBool):
    #reverseBool: false sorts in ascending order, true sorts in descending order
    foodListIn.sort(key=lambda x: eval('x.'+sortBy),reverse=reverseBool)
    