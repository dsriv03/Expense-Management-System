import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os


print('Welcome to Expenditure Management System.')
try: 
        pd.read_csv('users.csv')
except:
        print('IMPORTANT: This program creates additional files and sub-directories.')
        print('It is strongly advised to place this program in a seperate directory.')
        Users = []
        response1 = str(input("Is this program being used for personal records? (Yes/No)\n"))
        fnActive = True
        while fnActive == True:
            if response1 == 'No':
                response2 = int(input('How many records are being maintained?\n'))
                for i in range(response2):
                    Username = str(input('Name: '))
                    Users.append(Username)
                    ConfigDict = {'User':Username, 'MonthlyBudget':'not set'}
                    df = pd.DataFrame(ConfigDict,index=[0])
                    os.mkdir(os.path.join(os.getcwd(), Username))
                    df.set_index('User',inplace=True)
                    df.to_csv(os.path.join(os.getcwd(), Username, 'config.ini'))
                UsersDict = {'Users': Users}
                Userlist = pd.DataFrame(UsersDict)
                Userlist.to_csv('users.csv')
                fnActive = False
            elif response1 == 'Yes':
                Username = input('Name: ')
                ConfigData = {'User':Username, 'MonthlyBudget':'not set'}
                df = pd.DataFrame(ConfigData,index=[0])
                df.set_index('User')
                df.to_csv('config.ini')
                df.to_csv('users.csv')
                fnActive = False
            else:
                print('Invalid response.')
                

try:
    ActiveRecords = pd.read_csv('config.ini',index_col='User')
except:
    fnActive = True
    while fnActive == True:
        LoginUsername = input('Whose records would you like to access?\n')
        Usertable = pd.read_csv('Users.csv')
        if Usertable[Usertable['Users'] == LoginUsername].empty == True:
            print('Invalid name: Either the name is misspelt or records do not exist.')
        else:
            os.chdir(os.path.join(os.getcwd(), LoginUsername))
            ActiveRecords = pd.read_csv('config.ini',index_col=0)
            fnActive = False
LoginStatus = True


if datetime.date.today().strftime('%d') == 1:
    RequireInit = True
else:
    RequireInit = False
if ActiveRecords[ActiveRecords['MonthlyBudget'] == 'not set'].empty == False:
    RequireInit = True
if RequireInit == True:
    fnActive = True
    while fnActive == True:
        try:
            MonthlyBudget = int(input('Please enter the budget of this month: '))
            fnActive = False
        except:
            print('Entered data was invalid. Please enter a number.')
    MonthlyBudgetList = [MonthlyBudget]
    ActiveRecords['MonthlyBudget'] = MonthlyBudgetList
    try:
        Holdover = ActiveRecords['Holdover'][0]
    except:
        ActiveRecords['Holdover'] = [0]
        ActiveRecords['ActiveDay'] = [0]
        ActiveRecords['ActiveDayMoney'] = [0]
    ActiveRecords.to_csv('config.ini')


def AddRecord():
    NewItem = str(input('Enter the name of the item: '))
    fnActive = True
    while fnActive == True:
        try:
            NewQuantity = int(input('Enter the quantity:'))
            fnActive = False
        except:
            print('Input must be an integer.')
    fnActive = True
    while fnActive == True:
        try:
            NewCost = float(input('Enter the cost:'))
            fnActive = False
        except:
            print('Input can only be numeric or decimal.')
    Table.loc[NewItem] = [NewQuantity, NewCost]
    Table.to_csv(datetime.date.today().strftime('%B %d, %Y'))
    
def AlterRecord():
    PreAltRec = str(input('Which item would you like to alter?\n'))
    if Table.index.any != PreAltRec == True:
        print('Given item doesn not exist. Please check the items and spelling.')
    else:
        NewItem = str(input('Enter the name of the item: '))
        fnActive = True
        while fnActive == True:
            try:
                NewQuantity = int(input('Enter the quantity:'))
                fnActive = False
            except:
                print('Input must be an integer.')
        fnActive = True
        while fnActive == True:
            try:
                NewCost = float(input('Enter the cost:'))
                fnActive = False
            except:
                print('Input can only be numeric or decimal.')
        Table.drop(PreAltRec,inplace=True)
        Table.loc[NewItem] = [NewQuantity, NewCost]
        Table.to_csv(datetime.date.today().strftime('%B %d, %Y'))
        
def DeleteRecord():
    DelRec = str(input('Enter the item name you wish to delete: '))
    if Table.index.any != DelRec == True:
        print('No such item exists.')
    else:
        Table.drop(DelRec, axis=0,inplace=True)
        Table.to_csv(datetime.date.today().strftime('%B %d, %Y'))
def Graph():
    x_axis = []
    y_axis = []
    AmountLeftLine = []
    AmountLeftLineObj = DailyBudgetValue + SpentToday
    ShowGraphs = int(input("Enter 1 if you would like to see the graph of today's spending.\nEnter 2 if you would like to see the graph of this month's spending.\n"))
    if ShowGraphs == 1:
        for i in  range(Table.count()[0]):
            x_axis.append(Table.index[i])
            Cost = int(Table.iloc[i:i+1,]['Cost'])
            y_axis.append(Cost)
            AmountLeftLineObj = AmountLeftLineObj - Cost
            AmountLeftLine.append(int(AmountLeftLineObj))
        plt.bar(x_axis, y_axis, color='blue')
        plt.plot(AmountLeftLine, color='red', linewidth = 2)
        plt.show()
        print('The red line shows the remaining amount you have left for the day.')
    elif ShowGraphs == 2:
        x_axis = []
        y_axis = []
        AmountLeftLine = []
        AmountLeftLineObj = 0
        CurrentYear = int(datetime.date.today().strftime('%Y'))
        for i in range(DaysInMonth):
            SumDay = 0
            try:
                RecordToCheck = pd.read_csv(datetime.datetime(CurrentYear, CurrentMonth, i + 1).strftime('%B %d, %Y'))
                for j in range(RecordToCheck.count()[0]):
                    SumDay = SumDay + int(RecordToCheck.iloc[j:j+1,]['Cost'])
                    AmountLeftLineObj = AmountLeftLineObj + MonthlyBudgetValue/DaysInMonth - SumDay
                    AmountLeftLine.append(AmountLeftLineObj)
                    y_axis.append(SumDay)
                    x_axis.append(i + 1)
            except:
                x_axis.append(i + 1)
                y_axis.append(0)
                AmountLeftLine.append(AmountLeftLineObj + MonthlyBudgetValue/DaysInMonth) 
        print(y_axis)
        plt.bar(x_axis, y_axis, color='blue')
        plt.plot(AmountLeftLine, color='red', linewidth = 2)
        plt.show()
        print('The red line shows the remaining amount of money.')
    else:
        print('Invalid input.')


CurrentDate = datetime.date.today().strftime('%B %d, %Y')
MonthlyBudgetValue = ActiveRecords['MonthlyBudget'][0]
Holdover = ActiveRecords['Holdover'][0]
if ActiveRecords['ActiveDay'][0] != datetime.date.today() == True:
    ActiveRecords['Holdover'][0] = ActiveRecords['ActiveDayMoney'][0]
    ActiveRecords.to_csv('config.ini')
    
CurrentMonth = int(datetime.date.today().strftime('%m'))
if CurrentMonth == 1 or CurrentMonth == 3 or CurrentMonth == 5 or CurrentMonth == 7 or CurrentMonth == 8 or CurrentMonth == 10 or CurrentMonth == 12:
    DaysInMonth = int(31)
elif CurrentMonth == 4 or CurrentMonth == 6 or CurrentMonth == 9 or CurrentMonth == 11:
    DaysInMonth = 30
else:
    if int(datetime.date.today().strftime('%Y'))%4 != 0:
        DaysInMonth = 28
    else:
        DaysInMonth = 29

while LoginStatus == True:
    ActiveRecords['ActiveDay'] = datetime.date.today()
    ActiveRecords.to_csv('config.ini')
    try:
        Table = pd.read_csv(CurrentDate,index_col=0)
    except:
        Data = {'Items':[], 'Quantity':[], 'Cost':[]}
        Table = pd.DataFrame(Data)
        Table.set_index('Items',inplace=True)
    print('###################')
    if Table.empty == True:
        print('No records have been added yet.')
        print('No amount spent today.')
        DailyBudgetValue = Holdover + int(MonthlyBudgetValue/DaysInMonth)
        if Holdover > 0:
            print('You have an extra ', Holdover, 'to spend today.')
            if DailyBudgetValue > 0:
                print('You can safely spend ', DailyBudgetValue, 'today.')
            else:
                print('You have spent ', 0 - DailyBudgetValue, 'more than you planned to.')
        elif Holdover < 0:
            print('You cannot spend ', Holdover, 'today.')
            if DailyBudgetValue > 0:
                print('You can safely spend ', DailyBudgetValue, 'today.')
            else:
                print('You have spent ', 0 - DailyBudgetValue, 'more than you planned to.')
        SpentToday = 0
    else:
        print(Table)
        ItemNumber = Table.count()['Quantity']
        SpentToday = 0
        for i in range(ItemNumber):
            SpentToday = SpentToday + int(Table.iloc[i:i+1,:]['Cost'])
        print('Amount spent today is ',SpentToday)
        DailyBudgetValue = Holdover + int(MonthlyBudgetValue/DaysInMonth) - SpentToday
        if Holdover >= 0:
            print('You have an extra ', Holdover, 'to spend today.')
            if DailyBudgetValue > 0:
                print('You can safely spend ', DailyBudgetValue, 'today.')
            else:
                print('You have spent ', 0 - DailyBudgetValue, 'more than you planned to.')
        elif Holdover < 0:
            print('You cannot spend ', 0 - Holdover, 'today.')
            if DailyBudgetValue > 0:
                print('You can safely spend ', DailyBudgetValue, 'today.')
            else:
                print('You have spent ', 0 - DailyBudgetValue, 'more than you planned to.')

        ActiveRecords['ActiveDayMoney'] = [DailyBudgetValue]
        ActiveRecords.to_csv('config.ini')
    print('###################')
    print('Enter the number corresponding to the action you would like to do.')
    print('[1] - Add an item.')
    print('[2] - Alter a record.')
    print('[3] - Delete a Record.')
    print('[4] - Show Graphs.')
    print('[5] - Quit')
    CommandInput = int(input())
    
    if CommandInput == 1:
        AddRecord()
    elif CommandInput == 2:
        AlterRecord()
    elif CommandInput == 3:
        DeleteRecord()
    elif CommandInput == 4:
        Graph()
    elif CommandInput == 5:
        LoginStatus = False