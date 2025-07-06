from json import loads, dumps
from os.path import dirname, abspath, join
from os import listdir
from copy import copy, deepcopy

def recursiveDump(foodIn):
        foodDict=deepcopy(foodIn.__dict__)
        try:
            del foodDict['foodHolder']
        except:
            pass
        # if foodIn.constituents!=[]: 
        if 'constituents' in foodDict:
            dumpList=[]
            for food in foodDict['constituents']:
                foodDump_iter=recursiveDump(food)
                dumpList.append(foodDump_iter)
            foodDict['constituents']=dumpList
            # foodIn.constituents=dumpList
        if isinstance(foodDict['isConstituentOf'],str):
            isConstituentOfStr=foodDict['isConstituentOf']
        else:
            isConstituentOfStr=''
            try:
                if not isinstance(foodDict['isConstituentOf'][0],str):
                    for otherFood in foodDict['isConstituentOf']:
                        isConstituentOfStr+=otherFood.name+','
                    if isConstituentOfStr!='':
                        isConstituentOfStr=isConstituentOfStr[:-1]
                else:
                    for foodStr in foodDict['isConstituentOf']:
                        isConstituentOfStr+=foodStr+','
                    isConstituentOfStr=isConstituentOfStr[:-1]
            except:
                pass
        foodDict['isConstituentOf']=isConstituentOfStr
        foodDump=dumps(foodDict)
        foodDump=foodDump.replace('\\','')
        foodDump=foodDump.replace('"{','{')
        foodDump=foodDump.replace('}"','}')
        return foodDump
def recursiveLoad(jsonIn,allFoodDictionary,constituentOfDictionary):
    if type(jsonIn)==str:
        jsonDict=loads(jsonIn)
    else:
        jsonDict=jsonIn
    # if jsonDict['constituents']!=[]: 
    if 'constituents' in jsonDict:
        foodList=[]
        for foodEntry in jsonDict['constituents']:
            foodRetrieved=recursiveLoad(foodEntry,allFoodDictionary,constituentOfDictionary)
            if foodRetrieved.name not in constituentOfDictionary.keys():
                constituentOfDictionary[foodRetrieved.name]=[]
            constituentOfDictionary[foodRetrieved.name].append(jsonDict['name'])            
            if foodRetrieved not in foodList:
                foodList.append(foodRetrieved)
        # foodOut=foodItem(jsonDict['name'],jsonDict['quantity'],jsonDict['kcal'],jsonDict['protein'],jsonDict['carbs'],jsonDict['fat'],jsonDict['fibers'],constituents=[])
        jsonDict['constituents']=foodList
    #     foodOut=foodItem(jsonDict['name'],jsonDict['quantity'],jsonDict['kcal'],jsonDict['protein'],jsonDict['carbs'],jsonDict['fat'],jsonDict['fibers'],jsonDict['constituents'])        
    # else:
    foodOut=newOrExistingFood(jsonDict,allFoodDictionary)
    # foodOut=foodItem(jsonDict['name'],jsonDict['quantity'],jsonDict['kcal'],jsonDict['protein'],jsonDict['carbs'],jsonDict['fat'],jsonDict['fibers'],jsonDict['constituents'],jsonDict['notes'])
    return foodOut
def newOrExistingFood(jsonDict,allFoodDictionary):
    if 'constituents' not in jsonDict:
        food=foodItem(jsonDict['name'],jsonDict['quantity'],jsonDict['kcal'],jsonDict['protein'],jsonDict['carbs'],jsonDict['fat'],jsonDict['fibers'],jsonDict['notes'])      
    else:
        food=mixedFood()
        food.setName(jsonDict['name'])
        for qty,constituent in zip(jsonDict['constituentQuantities'],jsonDict['constituents']):
            food.addConstituent(constituent,qty)
        food.updateNotes(jsonDict['notes'])
        food.updateMacros()
    # # food=foodItem(jsonDict['name'],jsonDict['quantity'],jsonDict['kcal'],jsonDict['protein'],jsonDict['carbs'],jsonDict['fat'],jsonDict['fibers'],jsonDict['constituents'],jsonDict['notes'])    
    # if jsonDict['isConstituentOf']!='':
    #     for otherFoodStr in jsonDict['isConstituentOf'].split(','):
    #         food.makeConstituentOf(otherFoodStr)
    if jsonDict['name'] not in allFoodDictionary:
        allFoodDictionary[jsonDict['name']]=food
    else:
        while True:
            # dumpStr_food=recursiveDump(food)
            existingFood=allFoodDictionary[food.name]
            # dumpStr_existingFood=recursiveDump(existingFood)
            comparativeBool,foodToKeep=compareFoodStrs(food,existingFood)            
            if comparativeBool:
                if foodToKeep==existingFood:
                    food.removeFoodToFoodReferences()
                food=foodToKeep
                break
            else:
                newFoodName=food.name+'*'
                food.name=newFoodName
                if newFoodName not in allFoodDictionary.keys():
                    allFoodDictionary[newFoodName]=food
                    break
    return food
def compareFoodStrs(newFood,existingFood):
    def strIsolator(fStr):
        refStr='"isConstituentOf":'
        in1=fStr.find(refStr)+len(refStr)
        in2=fStr[in1:].find('",')
        constituentOfStr=fStr[in1:in1+in2]
        return fStr[:in1],fStr[in1+in2:],constituentOfStr
    fStr1=recursiveDump(newFood)
    fStr2=recursiveDump(existingFood)
    if fStr1==fStr2:
        return True,existingFood
    else:
        fStart1,fEnd1,constituentOfStr1=strIsolator(fStr1)
        fStart2,fEnd2,constituentOfStr2=strIsolator(fStr2)
        if fStart1==fStart2 and fEnd1==fEnd2:
            if len(constituentOfStr1)>len(constituentOfStr2):
                existingFood=newFood
            return True,existingFood
        else:
            return False,None

class foodHolder:
    def __init__(self,locationToSave=None,filename=str,allFoodDictionary=dict,constituentOfDictionary=dict) -> None:
        self.name=filename
        if locationToSave==None:
            self.saveLocation=dirname(abspath(__file__))
        else:
            self.saveLocation=locationToSave
        self.foodList=[]
        self.allFoodDictionary=allFoodDictionary
        self.constituentOfDictionary=constituentOfDictionary
    def appendFoodFromFile(self,loadFolder,filename):
        if self.name+'.json'==filename: #read file contents and add to foodList
            with open(join(loadFolder,self.name+'.json'),'r') as f:                    
                for row in f:
                    rowDict=loads(row)
                    # if rowDict['constituents']!=[]:
                    if 'constituents' in rowDict:
                        # rowFood=foodItem(rowDict['name'],rowDict['quantity'],rowDict['kcal'],rowDict['protein'],rowDict['carbs'],rowDict['fat'],rowDict['fibers'],constituents=None)                            
                        # for foodDict in rowDict['constituents']:
                        #     rowFood.constituents.append(foodItem(foodDict['name'],foodDict['quantity'],foodDict['kcal'],foodDict['protein'],foodDict['carbs'],foodDict['fat'],foodDict['fibers'],foodDict['constituents']))                                
                        # self.foodList.append(rowFood)
                        newFoodItem=recursiveLoad(row,self.allFoodDictionary,self.constituentOfDictionary)
                        # if rowFood not in self.foodList:
                        #     self.foodList.append(rowFood)
                        #läs in constituents separat och skapa foodItems för dem, se till att funkar även med nestade..antagligen rekursiv funktion, kolla om bara behöver rekursiv funktion för att spara, modifiera json-string som får ut från nestade foodItems så tar bort "" mellan nya items i listan...
                    else:
                        newFoodItem=newOrExistingFood(rowDict,self.allFoodDictionary)
                        # if rowDict['name'] not in self.allFoodDictionary.keys():
                        #     newFoodItem=foodItem(rowDict['name'],rowDict['quantity'],rowDict['kcal'],rowDict['protein'],rowDict['carbs'],rowDict['fat'],rowDict['fibers'],rowDict['constituents'],rowDict['notes'])
                        #     self.allFoodDictionary[rowDict['name']]=newFoodItem
                        # else:
                        #     newFoodItem=self.allFoodDictionary[rowDict['name']]
                    if newFoodItem not in self.foodList:
                        self.foodList.append(newFoodItem)
                        newFoodItem.assignFoodHolder(self)
    def addFood(self,food):
        self.foodList.append(food)
    def removeFood(self,food):
        try:
            self.foodList.remove(food)
        except:
            pass
    def saveToFile(self):
        with open(join(self.saveLocation,self.name+'.json'),'w') as f:
            for food in self.foodList:
                food_=deepcopy(food)
                if len(food.isConstituentOf)!=0:
                    isConstituentOfStr=''
                    for food__ in food.isConstituentOf:
                        isConstituentOfStr+=food__.name+','
                    isConstituentOfStr=isConstituentOfStr[:-1]
                    food_.isConstituentOf=isConstituentOfStr
                else:
                    food_.isConstituentOf=''
                # if food.constituents==[]:
                if not hasattr(food_,'constituents'):
                    foodDict=deepcopy(food_.__dict__)
                    try:
                        del foodDict['foodHolder']
                    except:
                        pass
                    f.write(dumps(foodDict)+'\n')
                else:
                    dumpStr=recursiveDump(food_)
                    f.write(dumpStr+'\n')

class foodItem:
    def __init__(self,name='',quantity=100,kcal=0,protein=0,carbs=0,fat=0,fibers=0,notes=''):
        self.name=name
        self.quantity=100
        self.protein=protein*quantity/100
        self.carbs=carbs*quantity/100
        self.fat=fat*quantity/100
        self.fibers=fibers*quantity/100
        self.kcal=kcal*quantity/100
        self.notes=notes
        self.isConstituentOf=[]
        self.macroStrs=['kcal','protein','carbs','fat','fibers']
    def getMacros(self):
        return [self.kcal,self.protein,self.carbs,self.fat,self.fibers]
    def updateNote(self,noteStr):
        self.notes=noteStr
    def updateMacros(self,qty,macroDict):
        for key in macroDict:
            self.__dict__[key]=macroDict[key]
        self.updateAttribute('quantity',qty)
    def updateAttribute(self,attributeStr,newAttributeValue):
        if attributeStr=='quantity':
            for macroStr in self.macroStrs:
                exec('self.'+macroStr+'=self.quantity/newAttributeValue*self.'+macroStr)
        else:
            self.__dict__[attributeStr]=newAttributeValue
        for food in self.isConstituentOf:
            food.updateMacros()
    def assignConstituentOfList(self,constituentOfList):
        self.isConstituentOf=constituentOfList
    def makeConstituentOf(self,constituentOf):
        self.isConstituentOf.append(constituentOf)
    def assignFoodHolder(self,foodHolder):
        self.foodHolder=foodHolder
    def removeFoodReference(self,foodToRemove):
        if foodToRemove in self.isConstituentOf:
            self.isConstituentOf.remove(foodToRemove)
    def removeFoodToFoodReferences(self):
        for food in self.isConstituentOf:
            food.removeFoodReference(self)
        try:
            self.foodHolder.foodList.remove(self)
        except:
            pass
    # def constituentOfStrsToFoods(self,allFoodDictionary:dict):
    #     if len(self.isConstituentOf)!=0 and isinstance(self.isConstituentOf[0],str):
    #         isConstituentOf_foods=[]
    #         for food in self.isConstituentOf:
    #             if isinstance(food,str):
    #                 try:
    #                     food_=allFoodDictionary[food]                        
    #                 except:
    #                     pass
    #             else:
    #                 food_=food
    #             if food_ not in isConstituentOf_foods:
    #                 isConstituentOf_foods.append(food_)                    
    #         self.isConstituentOf=isConstituentOf_foods
                

class mixedFood:
    def __init__(self):
        self.name=''
        self.constituents=[]
        self.isConstituentOf=[]
        self.constituentQuantities=[]
        self.notes=''
        self.macroStrs=['kcal','protein','carbs','fat','fibers']
        self.resetMacros()
    def setName(self,nameStr):
        self.name=nameStr
    def assignFoodHolder(self,foodHolder):
        self.foodHolder=foodHolder
    def assignConstituentOfList(self,constituentOfList):
        self.isConstituentOf=constituentOfList
    def addConstituent(self,constituent,constituentQuantity):
        self.constituents.append(constituent)
        self.constituentQuantities.append(constituentQuantity)
        self.updateMacros()
        constituent.makeConstituentOf(self)
        self.quantity=sum(self.constituentQuantities)
    def makeConstituentOf(self,constituentOf):
        self.isConstituentOf.append(constituentOf)
    def updateNotes(self,noteStr):
        self.notes=noteStr
    def resetMacros(self):
        self.quantity=0
        self.protein=0
        self.carbs=0
        self.fat=0
        self.fibers=0
        self.kcal=0
    def getMacros(self):
        return [self.kcal,self.protein,self.carbs,self.fat,self.fibers]
    def updateMacros(self):
        self.resetMacros()
        constituent_indices_to_remove=[]
        for i,(qty,constituent) in enumerate(zip(self.constituentQuantities,self.constituents)):
            self.quantity+=qty
            if constituent.quantity>0:      
                for macroStr,constituent_macro in zip(self.macroStrs,constituent.getMacros()):
                    exec('self.'+macroStr+'+=qty/constituent.quantity*constituent_macro')
            else:
                constituent_indices_to_remove.append(i)
        for i in constituent_indices_to_remove:
            del self.constituents[i]
            del self.constituentQuantities[i]
    def removeFoodReference(self,foodToRemove):
        if foodToRemove in self.isConstituentOf:
            self.isConstituentOf.remove(foodToRemove)
        if foodToRemove in self.constituents:
            removeIndex=self.constituents.index(foodToRemove)
            del self.constituents[removeIndex]
            del self.constituentQuantities[removeIndex]
        self.updateMacros()
    def removeFoodToFoodReferences(self):
        for food in self.isConstituentOf:
            food.removeFoodReference(self)
        for food in self.constituents:
            food.removeFoodReference(self)
        try:
            self.foodHolder.foodList.remove(self)
        except:
            pass
    def clearConstituents(self):
        for food in self.constituents:
            food.removeFoodReference(self)
        self.constituents.clear()
        self.constituentQuantities.clear()
        self.resetMacros()
            
class meal_holder:
    def __init__(self,name,locationToSave,allFoodDictionary,constituentOfDictionary):
        self.meal_dict={}
        self.tags=[]
        self.name=name
        self.allFoodDictionary=allFoodDictionary
        self.constituentOfDictionary=constituentOfDictionary
        if locationToSave==None:
            self.saveLocation=dirname(abspath(__file__))
        else:
            self.saveLocation=locationToSave
    def add_meal(self,meal_name,qtys,food_list):
        self.meal_dict[meal_name]={'foods':food_list,'quantities':qtys}
    def add_food_to_meal(self,meal_name,food):
        try:
            self.meal_dict[meal_name].append(food)
        except:
            print(f"{meal_name} not found in this meal holder")
    def remove_food_from_meal(self,meal_name,food):
        try:
            self.meal_dict[meal_name].remove(food)
        except:
            print(f"{meal_name} not found in this meal holder")
    def add_tag(self,tag):
        self.tags.append(tag)


    def saveToFile(self):
        with open(join(self.saveLocation,self.name+'.json'),'w') as f:
            f.write(f"Tags: {self.tags}\n")
            for meal_name,meal_dict in self.meal_dict.items():                
                f.write("\n")
                f.write(f"Meal: {meal_name}\n")
                for food,qty in zip(meal_dict['foods'],meal_dict['quantities']):
                    food_=deepcopy(food)
                    if len(food.isConstituentOf)!=0:
                        isConstituentOfStr=''
                        for food__ in food.isConstituentOf:
                            isConstituentOfStr+=food__.name+','
                        isConstituentOfStr=isConstituentOfStr[:-1]
                        food_.isConstituentOf=isConstituentOfStr
                    else:
                        food_.isConstituentOf=''
                    if not hasattr(food_,'constituents'):
                        foodDict=deepcopy(food_.__dict__)
                        try:
                            del foodDict['foodHolder']
                        except:
                            pass
                        dumpStr=dumps(foodDict)
                    else:
                        dumpStr=recursiveDump(food_)
                    f.write(f'{{"quantity": {qty},{dumpStr}}}\n')

    def append_meal_from_file(self,loadFolder,filename):
        if self.name+'.json'==filename: #read file contents and add to foodList
            with open(join(loadFolder,self.name+'.json'),'r') as f:
                tags_meals=f.read().strip().split('\n\n')
                tags_str=tags_meals[0]
                tags=tags_str[tags_str.find('[')+1:tags_str.find(']')].split(',')
                for tag in tags:
                    self.tags.append(tag)
                meals=tags_meals[1:]
                for meal in meals:
                    meal_name=meal[meal.find(': ')+2:meal.find('\n')]
                    meal_info_=meal[meal.find('\n')+1:]
                    food_list=[]
                    food_list_quantities=[]
                    for mi in meal_info_.split('}\n{'):
                        quantity=float(mi[mi.find(':')+1:mi.find(',')])
                        meal_info=mi[mi.find('{"name"'):]
                        if meal_info.endswith('}}'):
                            meal_info=meal_info[:-1]
                        mealDict=loads(meal_info)
                        if 'constituents' in mealDict:
                            newFoodItem=recursiveLoad(meal_info,self.allFoodDictionary,self.constituentOfDictionary)
                        else:
                            newFoodItem=newOrExistingFood(mealDict,self.allFoodDictionary)
                        food_list.append(newFoodItem)
                        food_list_quantities.append(quantity)
                    self.add_meal(meal_name,food_list_quantities,food_list)

#backend testing
afd={}
cd={}
m=meal_holder('test',None,afd,cd)
m.add_tag('tag1')
m.add_tag('tag2')
a=foodItem('a')
b=foodItem('b')
afd['a']=a
afd['b']=b
m.add_meal('ab',[10,20],[a,b])
mm=mixedFood()
mm.setName('mm')
mm.addConstituent(a,30)
mm.addConstituent(b,40)
afd['mm']=mm
cd['a']=[mm]
cd['b']=[mm]
m.add_meal('mm',[20],[mm])
m.saveToFile()
n=meal_holder('test',None,afd,cd)
import os
n.append_meal_from_file(os.path.dirname(__file__),'test.json')
1

# class foodItem:
#     def __init__(self,name='',quantity=100,kcal=0,protein=0,carbs=0,fat=0,fibers=None,constituents=[],notes='') -> None:
#         self.name=name
#         self.quantity=quantity
#         self.protein=protein
#         self.carbs=carbs
#         self.fat=fat
#         self.fibers=fibers
#         self.kcal=kcal
#         self.constituents=[]
#         self.notes=notes
#         self.willBeUpdated=False
#         self.isConstituentOf=[]
#         if constituents!=[]:
#             fiberSum=0
#             fiberInfoCounter=0
#             self.quantity=0
#             for food in constituents:
#                 self.quantity+=food.quantity
#                 self.protein+=food.protein
#                 self.carbs+=food.carbs
#                 self.fat+=food.fat
#                 self.kcal+=food.kcal
#                 # if food.fibers!=None:
#                 if food.completeFiberInfo:
#                     fiberSum+=food.fibers
#                     fiberInfoCounter+=1
#                 self.constituents.append(copy(food))
#             if fiberInfoCounter==len(constituents):
#                 self.completeFiberInfo=True                
#             else:
#                 self.completeFiberInfo=False
#             self.fibers=fiberSum
#             # self.completeFiberInfo=completeFiberInfo
#         else:
#             if fibers!=None:
#                 self.completeFiberInfo=True
#             else:
#                 self.completeFiberInfo=False
#     def showNutrients(self):
#         print(self.name+', '+str(self.quantity)+'g :',self.kcal,self.protein,self.carbs,self.fat,self.fibers)
#     def getFoodData(self):
#         return [self.quantity,self.kcal,self.protein,self.carbs,self.fat,self.fibers]
#     def showNutrients_constituents(self):
#         for constituent in self.constituents:
#             constituent.showNutrients()
#     def updateNote(self,noteStr):
#         self.notes=noteStr
#     def changeQuantity(self,newQuantity):
#         self.protein=self.protein*newQuantity/self.quantity
#         self.carbs=self.carbs*newQuantity/self.quantity
#         self.fat=self.fat*newQuantity/self.quantity
#         if self.fibers!=None:
#             self.fibers=self.fibers*newQuantity/self.quantity
#         self.kcal=self.kcal*newQuantity/self.quantity
#         for constituent in self.constituents:
#             constituent.changeQuantity(newQuantity)
#         self.quantity=newQuantity
#     def toBeUpdated(self):
#         self.willBeUpdated=True
#         for food in self.isConstituentOf:
#             food.toBeUpdated()
#     def assignConstituentOfList(self,constituentOfList):
#         self.isConstituentOf=constituentOfList

def sortFoodList(foodListIn,sortBy,reverseBool):
    #reverseBool: false sorts in ascending order, true sorts in descending order
    foodListIn.sort(key=lambda x: eval('x.'+sortBy),reverse=reverseBool)
    