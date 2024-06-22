#fixa completeFiberInfo, blir skumt då har nested fooditems och sparar om- antagligen pga att bara tittar lokalt om har fibervärde som ej är noll och ej att alla consituents också har det!

# import os
# import operator #for fetching attributes name to sort objects..
# import json
# import copy
# import tkinter as tk

from backend.backend import *
from os.path import exists
from os import remove

loadDir=dirname(abspath(__file__))


# allFoodDictionary=dict()
# beef=foodItem('beef',100,150,20,5,8,notes='this is beff')
# beef.updateAttribute('quantity',50)
# chicken=foodItem('chicken',100,100,18,3,4,notes='CHICKEN\\yo!')
# carrot=foodItem('carrot',100,20,1,5,0.1,2,notes='healthy')
# cabbage=foodItem('cabbage',100,18,0.5,3,4,1,notes='yummy')

# meat=foodHolder(loadDir,'meat',allFoodDictionary)
# meat.addFood(beef)
# meat.addFood(chicken)
# meat.saveToFile()

# mFood=mixedFood()
# mFood.setName('mFood')
# mFood.addConstituent(beef,50)
# mFood.addConstituent(carrot,200)
# print(mFood.getMacros())

# testi=foodHolder(filename='testi',allFoodDictionary=allFoodDictionary,locationToSave=loadDir)
# beef.updateAttribute('quantity',500)
# testi.addFood(beef)
# testi.addFood(mFood)
# mFood2=deepcopy(mFood)
# mFood3=mixedFood()
# mFood3.addConstituent(mFood2,50)
# testi.addFood(mFood2)
# testi.addFood(mFood3)
# testi.saveToFile()

fH_dict=dict()
allFoodDictionary=dict()
constituentOfDictionary=dict()
for f in listdir(loadDir):
    if f.endswith('.json'):
        foodHolderName=f.split('.')[0]
        fH_dict[foodHolderName]=foodHolder(locationToSave=loadDir,filename=f[0:-5],allFoodDictionary=allFoodDictionary,constituentOfDictionary=constituentOfDictionary)
        fH_dict[foodHolderName].appendFoodFromFile(loadDir,f)

loadDir=dirname(abspath(__file__))
fH_dict=dict()
foodAttributes=['name','kcal','quantity','protein','carbs','fat','fibers','constituents']
clickList=[]
clickList_details=[]
from frontend.GUIassembler import *
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
    self.foodDisplayPanel.populatePanel(foodStack,foodAttributes,foodContainerName,'foodContainer',clickList)
    self.stackLayout.setCurrentIndex(1)
def updateClickList(clickText,foodID):
    if clickText in clickList:
        priorInd=clickList.index(clickText)
        del clickList[priorInd+1:]
        del clickList_details[priorInd+1:]
    else:
        clickList.append(clickText)
        clickList_details.append(('food',foodID))
def tableItemOnClick_ext(self,item):
    if self.activeDisplayType=='foodContainer':
        self.foodListHolder.constituentList.selectRow(item.row())
        foodID=self.foodListHolder.constituentList.item(item.row(),self.foodListHolder.constituentList.columnCount()-1).text()
        holderType=self.foodListHolder
        itemText=holderType.constituentList.item(item.row(),0).text()    
    elif self.activeDisplayType=='foodMix':
        self.foodMixHolder.constituentList.selectRow(item.row())
        foodID=self.foodMixHolder.constituentList.item(item.row(),self.foodMixHolder.constituentList.columnCount()-1).text()    
        holderType=self.foodMixHolder
        itemText=holderType.constituentList.item(item.row(),0).text()    
    else:
        self.foodItemHolder.ingridientList.selectRow(item.row())
        foodID=self.foodItemHolder.ingridientList.item(item.row(),self.foodItemHolder.ingridientList.columnCount()-1).text()    
        holderType=self.foodItemHolder
        itemText=holderType.ingridientList.item(item.row(),0).text()    
    # for i in range(6):
    #     holderType.constituentList.item(item.row(),i).setForeground(QBrush(Qt.GlobalColor.green,Qt.BrushStyle.SolidPattern))
    updateClickList(itemText,foodID)
    # rowStr=''
    # for i in range(5):
    #     rowStr+=','+self.foodListHolder.constituentList.item(item.row(),i).text()
    # print(rowStr)
    # print(self.constituentList.item(item.row(),self.constituentList.columnCount()-1).text())    
    if isinstance(self.foodDict[foodID],mixedFood):
        foodStack=getFoodStack(self.foodDict[foodID].constituents,self.foodDict)
    else:
        foodStack=False
    if foodStack:
        # self.populatePanel(foodStack,foodAttributes,self.foodDict[foodID].name,'foodMix',clickList,notes='',dataList2=self.foodDict[foodID].getFoodData())
        self.populatePanel(foodStack,foodAttributes,self.foodDict[foodID].name,'foodMix',clickList,notes='',dataList2=[self.foodDict[foodID].quantity]+self.foodDict[foodID].getMacros())
    else:
        # self.populatePanel(self.foodDict[foodID].getFoodData(),foodAttributes,self.foodDict[foodID].name,'foodItem',clickList,self.foodDict[foodID].notes)
        # self.populatePanel([self.foodDict[foodID].quantity]+self.foodDict[foodID].getMacros(),foodAttributes,self.foodDict[foodID].name,'foodItem',clickList,self.foodDict[foodID].notes,dataList2=[[f.name]+f.getMacros() for f in self.foodDict[foodID].isConstituentOf])
        self.populatePanel([self.foodDict[foodID].quantity]+self.foodDict[foodID].getMacros(),foodAttributes,self.foodDict[foodID].name,'foodItem',clickList,self.foodDict[foodID].notes,dataList2=getFoodStack(self.foodDict[foodID].isConstituentOf,self.foodDict))
        # self.kcal,self.protein,self.carbs,self.fat,self.fibers
def closeDisplayPanel_external(self):    
    clickList.clear()
    clickList_details.clear()
    self.extScroll.clear()
    for foodHolderName in fH_dict.keys():
        self.addExtFCtoScroll(foodHolderName)
def hierarcyClick(self,item):
    hierarcyIndex=clickList.index(item.text())
    if clickList_details[hierarcyIndex][0]=='foodContainer':
        foodContainerName=clickList[hierarcyIndex]
        fH_clicked_contents=fH_dict[foodContainerName].foodList
        foodStack=getFoodStack(fH_clicked_contents,self.foodDict)
        del clickList[1:]
        del clickList_details[1:]
        self.populatePanel(foodStack,foodAttributes,foodContainerName,'foodContainer',clickList)
    else:
        foodID=clickList_details[hierarcyIndex][1]
        updateClickList(item.text(),foodID)
        if isinstance(self.foodDict[foodID],mixedFood):
            foodStack=getFoodStack(self.foodDict[foodID].constituents,self.foodDict)
        else:
            foodStack=False
        if foodStack:
            self.populatePanel(foodStack,foodAttributes,self.foodDict[foodID].name,'foodMix',clickList,notes='',dataList2=[self.foodDict[foodID].quantity]+self.foodDict[foodID].getMacros())
        else:
            # self.populatePanel([self.foodDict[foodID].quantity]+self.foodDict[foodID].getMacros(),foodAttributes,self.foodDict[foodID].name,'foodItem',clickList,self.foodDict[foodID].notes)
            self.populatePanel([self.foodDict[foodID].quantity]+self.foodDict[foodID].getMacros(),foodAttributes,self.foodDict[foodID].name,'foodItem',clickList,self.foodDict[foodID].notes,dataList2=getFoodStack(self.foodDict[foodID].isConstituentOf,self.foodDict))
            
foodContainerPanel.extFCclicked_external=extFCclicked_ext
foodDisplayPanel.tableItemClick_external=tableItemOnClick_ext
foodContainerPanel.closeDisplayPanel_external=closeDisplayPanel_external
foodDisplayPanel.hierarcyClick_external=hierarcyClick

def createFC(self):
    foodHolderName=self.searchField.text()
    fH_dict[foodHolderName]=foodHolder(locationToSave=loadDir,filename=foodHolderName,allFoodDictionary=allFoodDictionary,constituentOfDictionary=constituentOfDictionary)
    self.addExtFCtoScroll(foodHolderName)
    
foodContainerPanel.createFC=createFC

nonUniqueStr='There\'s already a food item with this name, please change it!'
fcEnterStr='Enter existing food container!'
def addFoodButtonAction(self):
    qtys=[]
    for ql in self.quantityLineEdits:
        qtys.append(float(ql.text()))
    if self.nameEntry.text() not in allFoodDictionary.keys() and self.nameEntry.text()!=nonUniqueStr:
        if self.foodContainerScroll.entryField.text() in fH_dict.keys():            
            newFood=foodItem(name=self.nameEntry.text(),quantity=qtys[0],kcal=qtys[1],protein=qtys[2],carbs=qtys[3],fat=qtys[4],fibers=qtys[5],notes=self.notes.toPlainText())
            allFoodDictionary[self.nameEntry.text()]=newFood
            fH_dict[self.foodContainerScroll.entryField.text()].addFood(newFood)
            for iter,ql in enumerate(self.quantityLineEdits):
                if iter==0:
                    ql.setText('100')
                else:
                    ql.setText('0')
                self.nameEntry.setText('')
                self.foodContainerScroll.entryField.setText('')
                self.notes.setPlainText('')
        else:
            self.foodContainerScroll.entryField.setText(fcEnterStr)
    else:
        self.nameEntry.setText(nonUniqueStr)

addFoodPanel.addButtonAction=addFoodButtonAction

def onClosingApplication(self):
    for fhdName in fH_dict.keys():
        fH_dict[fhdName].saveToFile()
def repeatLastHierarchyClick(self):
    if len(clickList)!=0:
        self.foodContainerPanel.foodDisplayPanel.hierarcyClick_external(QLabel(clickList[-1]))
mainWindow.additionalCloseEvents=onClosingApplication
mainWindow.foodContainerPanelUpdate=repeatLastHierarchyClick
foodItemFields=['quantity','kcal','protein','carbos','fat','fibers']
def editFoodItem(self):
    foodItem=allFoodDictionary[self.foodItemHolder.displayLabel.text()]
    if self.sender()==self.foodItemHolder.noteArea:
        if foodItem.notes!=self.foodItemHolder.noteArea.toPlainText():
            currentText=self.foodItemHolder.noteArea.toPlainText()+''
            foodItem.updateNote(currentText)
            # self.foodItemHolder.noteArea.clear()
            self.foodItemHolder.noteArea.setPlainText(currentText)

    else:        
        fieldIndex=self.foodItemHolder.qtyLineEdits.index(self.sender())
        foodItem.updateAttribute(foodItemFields[fieldIndex],float(self.sender().text()))
    self.hierarcyClick_external(QLabel(clickList[-1]))
def foodItemNoteKeyPressEvent(self):
    foodItem=allFoodDictionary[self.foodItemHolder.displayLabel.text()]
    foodItem.updateNote(self.foodItemHolder.noteArea.toPlainText())
    cursor=self.foodItemHolder.noteArea.textCursor()
    cursorPosition=cursor.position()
    self.hierarcyClick_external(QLabel(clickList[-1]))          
    cursor.setPosition(cursorPosition,QTextCursor.MoveMode.MoveAnchor)
    self.foodItemHolder.noteArea.setTextCursor(cursor)    
    # cursor.movePosition(cursorPosition,QTextCursor.MoveMode.KeepAnchor)
foodDisplayPanel.foodItemNoteKeyPressEvent=foodItemNoteKeyPressEvent
foodDisplayPanel.foodItemEdits=editFoodItem

def addFood_populateFoodContainers(self):
    self.foodContainerScroll.clearScrollList()
    for fhName in fH_dict.keys():
        self.foodContainerScroll.addToScrollList(fhName)
def addFood_populateFoods(self):
    self.nameEntry.clearScrollList()
    for fName in allFoodDictionary.keys():
        self.nameEntry.addToScrollList(fName)
addFoodPanel.populateFoodContainers=addFood_populateFoodContainers
addFoodPanel.populateFoods=addFood_populateFoods

def mixFood_populateFoods(self):
    self.nameEntry.clearScrollList()
    self.ingridientEntry.clearScrollList()
    for fName in allFoodDictionary.keys():
        self.nameEntry.addToScrollList(fName)
        self.ingridientEntry.addToScrollList(fName)
mixFoodPanel.populateFoods=mixFood_populateFoods
mixFoodPanel.populateFoodContainers=addFood_populateFoodContainers
def addIngridient(self):    
    try:
        qty=float(self.ingridientQuantityEntry.text())
        if qty>=0:
            ingridientMacros=allFoodDictionary[self.ingridientEntry.text()].getMacros()
            nIngridients=self.ingridientScroll.rowCount()    
            self.ingridientScroll.setRowCount(nIngridients+1)            
            nameCellEntry=QTableWidgetItem(self.ingridientEntry.text())
            nameCellEntry.setFlags(Qt.ItemFlag.NoItemFlags)
            nameCellEntry.setForeground(QColor(0,0,0))
            self.ingridientScroll.setItem(nIngridients,0,nameCellEntry)
            self.ingridientScroll.setItem(nIngridients,1,QTableWidgetItem(self.ingridientQuantityEntry.text()))
            self.quantityStatLabels[0].setText(str(float(self.quantityStatLabels[0].text())+qty))
            for i,cellEntry in enumerate(ingridientMacros):
                macroValue=round(cellEntry*qty/100,2)
                cellItem=QTableWidgetItem(str(macroValue))
                cellItem.setForeground(QColor(0,0,0))
                cellItem.setFlags(Qt.ItemFlag.NoItemFlags) 
                self.quantityStatLabels[i+1].setText(str(round(float(self.quantityStatLabels[i+1].text())+macroValue,2)))
                self.ingridientScroll.setItem(nIngridients,i+2,cellItem)
    except:
        pass
def quantityUpdated(self):
    if self.ingridientScroll.currentItem() is not None:        
        selectedRowIndex=self.ingridientScroll.currentRow()
        selectedFoodMacros=allFoodDictionary[self.ingridientScroll.item(selectedRowIndex,0).text()].getMacros()        
        newQuantity=float(self.ingridientScroll.currentItem().text())/100
        try:
            currentQuantity=float(self.ingridientScroll.item(selectedRowIndex,2).text())/selectedFoodMacros[0]
        except:
            currentQuantity=self.lastEnteredQuantity
        if newQuantity<0:
            newQuantity=currentQuantity
            self.ingridientScroll.currentItem().setText(str(currentQuantity*100))
        self.quantityStatLabels[0].setText(str(round(float(self.quantityStatLabels[0].text())-100*currentQuantity+100*newQuantity,2)))
        for i,macro in enumerate(selectedFoodMacros):
            self.quantityStatLabels[i+1].setText(str(round(float(self.quantityStatLabels[i+1].text())-macro*currentQuantity+macro*newQuantity,2)))
            self.ingridientScroll.item(selectedRowIndex,i+2).setText(str(round(macro*newQuantity,2)))
def quantityEntered(self):
    if self.ingridientScroll.currentItem() is not None:
        self.lastEnteredQuantity=float(self.ingridientScroll.currentItem().text())/100
def deleteIngridient(self):
    if self.ingridientScroll.currentItem() is not None:  
        rowIndex=self.ingridientScroll.currentRow()
        for i in range(self.ingridientScroll.columnCount()-1):
            self.quantityStatLabels[i].setText(str(float(self.quantityStatLabels[i].text())-float(self.ingridientScroll.item(rowIndex,i+1).text())))
        self.ingridientScroll.removeRow(rowIndex)
mixFoodPanel.addIngridient=addIngridient
mixFoodPanel.quantityUpdated=quantityUpdated
mixFoodPanel.quantityEntered=quantityEntered
mixFoodPanel.deleteIngridient=deleteIngridient

def addMixed(self):    
    if self.nameEntry.text() not in allFoodDictionary.keys() and self.nameEntry.text()!=nonUniqueStr:
        if self.foodContainerScroll.entryField.text() in fH_dict.keys():            
            newFood=mixedFood()
            newFood.setName(self.nameEntry.text())
            
            self.ingridientScroll.columnCount()
            while self.ingridientScroll.rowCount()>0:
                newFood.addConstituent(allFoodDictionary[self.ingridientScroll.item(0,0).text()],float(self.ingridientScroll.item(0,1).text()))
                self.ingridientScroll.removeRow(0)
            newFood.updateNotes(self.noteArea.toPlainText())

            for quantityLabel in self.quantityStatLabels:
                quantityLabel.setText('0')
            
            allFoodDictionary[self.nameEntry.text()]=newFood
            fH_dict[self.foodContainerScroll.entryField.text()].addFood(newFood)
            
            self.nameEntry.setText('')
            self.foodContainerScroll.entryField.setText('')
            self.noteArea.setPlainText('')
        else:
            self.foodContainerScroll.entryField.setText(fcEnterStr)
    else:
        self.nameEntry.setText(nonUniqueStr)
mixFoodPanel.addMixedFoodToFoodContainer=addMixed
def deleteFunction(self):
    print(self.activeDisplayType)
    if self.activeDisplayType=='foodContainer':
        print(self.activeDisplayType,self.panelTitle,fH_dict[self.panelTitle])
        del fH_dict[self.panelTitle]        
        if exists(self.panelTitle+'.json'):
            remove(self.panelTitle+'.json')
        self.foodListHolder.closeButton.click()
    else:
        if self.activeDisplayType=='foodMix':
            activeDisplay=self.foodMixHolder
        else:
            activeDisplay=self.foodItemHolder        
        allFoodDictionary[self.panelTitle].removeFoodToFoodReferences()
        del allFoodDictionary[self.panelTitle]
        self.hierarcyClick_external(activeDisplay.hierarcyScroll.item(activeDisplay.hierarcyScroll.count()-2))        
        
foodDisplayPanel.deleteButtonAction=deleteFunction

######################          FIXA DETTA          ############################################
#i mixed food panel, ha add ingridient å ingridient quantity på samma rad å add to food container på rad under, notearea därunder å minska tomrum
#lägg till så ser notes å constituent of i mixed foodpanel
#gör separat script för fooddisplaypanel å displaywidgetcreator
#fixa ny panel där kan göra samling av måltider:
#-batcha upp separata mål
#-möjlighet att ha target macros att jfr m
#-piechart över hur kalorier är fördelade
#-på nåt sätt kunna nesta i godtyckligt antal nivåer



#läser in unika foodItems och länkar likadana som ingredienser mellan olika foods
#lägger till * i slutet av namn på foodItem m samma namn men annorlunda makros
#problem: qty är attribut av food, så om har 50 g beef i en och 100 g beef i en annan kommer dessa foodItems ses som olika även fast utgår från samma beef
#->implementera separat foodItem klass som bara har /qty some attribut och separat mixFoodItem klass där har qty av constituents som attribut
#-kommer behöva ändra om hur läser in foods i gui
#-mindre ändringar i hur läser in och sparar mat i backend

#inläsningsstruktur:
#läs in som nu, alla foodItems läggs i dictionary: namn=nyckel, objekt=värde
#-duplicate-namn spara namn i separat lista och skapa lista med de itemsen i dictionary, efter läst in alla loopa igenom lista och prompta användare om att ge unika namn
#--då läser in constituents, kolla om finns med samma makros i dictionary och länka i sånt fall till det foodItem ist för att skapa nytt men fortsätt gå igenom nestade constituents, lägg till i dictonary om ej finns med
#-ytterligare en dictionary med namn=nyckel, värde=lista m foodItems de ingår i 
#--då uppdaterar värde i gui, ändra makron i foodItem och kör sen uppdaterindsfkn (nedan) för alla foodItems som foodItem ingår i från andra dictionaryn
#lägg till fkn i foodItem som uppdaterar deras makros (loopa igenom constituents om har)

#next up: 
# editera makros för foodItems (för foodMix ska dock bara gå att editera qty av constituents ej makros direkt) samt spara de nya värdena, även i filerna där de ligger!
# add food
# mix foods
# döpa om duplicate names, memoization?, så ex. carrot bara kan svara mot en sorts makros

app=frontendSetup()
app.mW.foodContainerPanel.extFCclicked_set()

allFoodDictionary=dict()
constituentOfDictionary=dict()
for f in listdir(loadDir):
    if f.endswith('.json'):
        foodHolderName=f.split('.')[0]
        fH_dict[foodHolderName]=foodHolder(locationToSave=loadDir,filename=f[0:-5],allFoodDictionary=allFoodDictionary,constituentOfDictionary=constituentOfDictionary)
        fH_dict[foodHolderName].appendFoodFromFile(loadDir,f)
        app.mW.foodContainerPanel.addExtFCtoScroll(foodHolderName)
# sortFoodList(fH_dict['meat'].foodList,'kcal',False)
# for food in fH_dict['meat'].foodList:
#     food.showNutrients()
    
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