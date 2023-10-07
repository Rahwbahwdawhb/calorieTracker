#fixa completeFiberInfo, blir skumt då har nested fooditems och sparar om- antagligen pga att bara tittar lokalt om har fibervärde som ej är noll och ej att alla consituents också har det!

# import os
# import operator #for fetching attributes name to sort objects..
# import json
# import copy
# import tkinter as tk

from backend import *



beef=foodItem('beef',100,150,20,5,8,notes='this is beff')
chicken=foodItem('chicken',100,100,18,3,4,notes='CHICKEN\\yo!')
carrot=foodItem('carrot',100,20,1,5,0.1,2,notes='healthy')
cabbage=foodItem('cabbage',100,18,0.5,3,4,1,notes='yummy')
meat=foodHolder(None,'meat')
meat.addFood(beef)
meat.addFood(chicken)
meat.saveToFile()
from copy import copy
beef2=copy(beef)
beef2.changeQuantity(50)
carrot2=copy(carrot)
carrot2.changeQuantity(150)
combo=foodItem(name='combo',constituents=[beef2,carrot2])
combo2=copy(combo)
combo3=foodItem(name='combo3',constituents=[combo2,carrot2])
combo.showNutrients()
combo.showNutrients_constituents()
testi=foodHolder(filename='testi')
# for food in testi.foodList:
#     food.showNutrients()
#     food.showNutrients_constituents()
testi.addFood(combo)
testi.addFood(combo3)
testi.saveToFile()
# for m in meat.foodList:
#     m.showNutrients()


loadDir=dirname(abspath(__file__))
fH_dict=dict()
foodAttributes=['name','quantity','protein','carbs','fat','fibers','kcal','constituents']
clickList=[]
clickList_details=[]
from frontend import *
# import time
def getFoodStack(foodList,foodDict):
    foodStack=[]
    for food in foodList:
        foodID=str(id(food))
        loc=locals()
        foodData=[str(eval('food.'+attr,loc)) for attr in foodAttributes[0:-1]]
        foodData.append(foodID)
        foodDict[foodID]=food
        foodStack.append(foodData)
    return foodStack
def extFCclicked_ext(self,item):
    # data = [['1','2','3','4','abc'],['5','6','7','8','def'],['4','3','2','1','ghi']]
    # self.foodDisplayPanel.populatePanel(data,['w','x','y','z'])
    foodContainerName=item.text()
    fH_clicked_contents=fH_dict[foodContainerName].foodList
    self.foodDisplayPanel.foodDict=dict()
    foodStack=getFoodStack(fH_clicked_contents,self.foodDisplayPanel.foodDict)
        # del foodData
    # print(foodStack)
    clickList.append(foodContainerName)
    clickList_details.append(('foodContainer',''))
    self.foodDisplayPanel.populatePanel(foodStack,foodAttributes,foodContainerName,True,clickList)
    self.stackLayout.setCurrentIndex(1)
def updateClickList(clickText,foodID):
    if clickText in clickList:
        priorInd=clickList.index(clickText)
        del clickList[priorInd+1:]
        del clickList_details[priorInd+1:]
    else:
        clickList.append(clickText)
        clickList_details.append(('food',foodID))
def onClick_ext(self,item):
    self.foodListHolder.constituentList.selectRow(item.row())
    foodID=self.foodListHolder.constituentList.item(item.row(),self.foodListHolder.constituentList.columnCount()-1).text()    
    updateClickList(item.text(),foodID)
    rowStr=''
    for i in range(5):
        rowStr+=','+self.foodListHolder.constituentList.item(item.row(),i).text()
    # print(rowStr)
    # print(self.constituentList.item(item.row(),self.constituentList.columnCount()-1).text())    
    foodStack=getFoodStack(self.foodDict[foodID].constituents,self.foodDict)
    if foodStack:
        self.populatePanel(foodStack,foodAttributes,self.foodDict[foodID].name,True,clickList)
    else:
        self.populatePanel(self.foodDict[foodID].getFoodData(),foodAttributes,self.foodDict[foodID].name,False,clickList,self.foodDict[foodID].notes)
        # self.kcal,self.protein,self.carbs,self.fat,self.fibers
def resetClickHistory(self):
    clickList.clear()
    clickList_details.clear()
def hierarcyClick(self,item):
    hierarcyIndex=clickList.index(item.text())
    if clickList_details[hierarcyIndex][0]=='foodContainer':
        foodContainerName=clickList[hierarcyIndex]
        fH_clicked_contents=fH_dict[foodContainerName].foodList
        foodStack=getFoodStack(fH_clicked_contents,self.foodDict)
        del clickList[1:]
        del clickList_details[1:]
        self.populatePanel(foodStack,foodAttributes,foodContainerName,True,clickList)
        print('foodContainer')
    else:
        foodID=clickList_details[hierarcyIndex][1]
        updateClickList(item.text(),foodID)
        foodStack=getFoodStack(self.foodDict[foodID].constituents,self.foodDict)
        if foodStack:
            self.populatePanel(foodStack,foodAttributes,self.foodDict[foodID].name,True,clickList)
        else:
            self.populatePanel(self.foodDict[foodID].getFoodData(),foodAttributes,self.foodDict[foodID].name,False,clickList,self.foodDict[foodID].notes)
foodContainerPanel.extFCclicked_external=extFCclicked_ext
foodDisplayPanel.externalFunction=onClick_ext
foodContainerPanel.resetClickHistory_external=resetClickHistory
foodDisplayPanel.hierarcyClick_external=hierarcyClick
#next up: 
# makros av det klickat på efter foodContainer (nu endast för enstaka foodItems, ska även vara för ex combo -ska dock bara gå att editera qty av constituents ej makros direkt)
# editera makros för foodItems samt spara de nya värdena, även i filerna där de ligger!
# add food
# mix foods
# döpa om duplicate names, memoization?, så ex. carrot bara kan svara mot en sorts makros

app=frontendSetup()
app.mW.foodContainerPanel.extFCclicked_set()
app.mW.foodContainerPanel.foodDisplayPanel.external_onClick()

for f in listdir(loadDir):
    if f.endswith('.json'):
        foodHolderName=f.split('.')[0]
        fH_dict[foodHolderName]=foodHolder(loadDir,f[0:-5])
        fH_dict[foodHolderName].appendFoodFromFile(loadDir,f)
        app.mW.foodContainerPanel.addExtFCtoScroll(foodHolderName)
sortFoodList(fH_dict['meat'].foodList,'kcal',False)
for food in fH_dict['meat'].foodList:
    food.showNutrients()
    
app.startGUI()
1

# # print(type(meat.foodList))
# beef.showNutrients()
# cabbage.showNutrients()
# testFH=foodHolder(None,'testFH')



#fixa: 
# så sparas ok då har combined foods-så finns records av constituents också..och att de återskapas som objekt
# referensintag och hur mkt har kvar tills uppnått

# def main():
#     mainWindow=tk.Tk()
#     mainWindow.title('Calorie Tracker')
#     screenWidth=mainWindow.winfo_screenwidth()
#     screenHeight=mainWindow.winfo_screenheight()
#     windowScale=0.5
#     windowWidth=int(screenWidth*windowScale)
#     windowHeight=int(screenHeight*windowScale)
#     centerX=int(screenWidth/2-windowWidth/2)
#     centerY=int(screenHeight/2-windowHeight/2)
#     mainWindow.geometry(f'{windowWidth}x{windowHeight}+{centerX}+{centerY}')
#     # mainWindow.attributes('-alpha',0.5)
#     mainWindow.mainloop()

# if __name__=='__main__':
#     main()