from node import Node
#برای اندازه گیری زمان اجرای الگوریتم 
from time import process_time


class AmplitudeAlgorithm:
    def __init__(self, world):
        self.emptyNode = Node(None, None, "first father", -1, 0, 0, 0) #ایجاد یک گره خالی به عنوان گره پایه یا والد اصلی
        self.firstNode = Node(world, self.emptyNode, " ", 0, 0, 0, 0) #نگه داشتن وضعیت اولیه تام در خود 
        self.tomPos = self.firstNode.searchForTom() #پیدا کردن موقعیت تام در هزارتو
        self.stack = [self.firstNode] #نگه داشتن لیستی از گره های در انتظار پردازش ، که در ابتدا فقط شامل گره شروع است 
        self.computingTime = "" # ذخیره زمان اجرا 
        # word استخراج ابعاد(طول و عرض) هزار تو از ماتریس  
        self.length_world = world.shape[0]
        self.height_world = world.shape[1]

    #دو تابع زیر برای دریافت و تنظیم زمان اجرای الگوریتم استفاده میشوند 
    def getComputingTime(self):
        return self.computingTime

    def setComputingTime(self, computingTime):
        self.computingTime = computingTime

    #این تابع مسول اجرای الگوریتم جست و جو است 
    #مراحل کلی ان شامل محاسبه زمان اجرا الگوریتم و جستجو در هزار تو و چاپ نتایج


    def start(self):
        startTime = process_time() #ذخیره زمان شروع اجرا الگوریتم

        stack = self.stack #استکی که شامل گره های در انتظار پذیرش، در اینجا فقط شامل گره شروع
        tomPos = self.tomPos #نگه داری موقعیت تام
        currentNode = stack[0] # انتخاب اولین گره به عنوان گره فعلی
        expandedNodes = 0 #تعداد گره های باز شده 
        depth = 0 #عمق جستجو


        # TO DO: implement your code here , don't forget to update stack, currentNode and depth
        while stack and not currentNode.isGoal():

            currentNode = stack.pop(0) #delete currentNode from top of the stack
            tomPos = currentNode.getTomPos() 
            expandedNodes += 1

            #بررسی حرکت به سمت راست
            if tomPos[1] + 1 < self.length_world and currentNode.getState()[tomPos[0], tomPos[1] + 1] != 1:
                son = Node(currentNode.getState(), currentNode, "right", currentNode.getDepth() + 1, currentNode.getCost(), currentNode.getStar(), currentNode.getFlower())
                right = son.rightMovement(tomPos)
                son.setNewCost(right)
                son.setTomPos(right)
                son.moveRight(tomPos)
                if son.compareCicles2(right):
                    stack.append(son)  # اضافه کردن به انتهای استک
                    if son.getDepth() > depth:
                        depth = son.getDepth()

            # بررسی حرکت به سمت چپ
            if tomPos[1] - 1 >= 0 and currentNode.getState()[tomPos[0], tomPos[1] - 1] != 1:
                son = Node(currentNode.getState(), currentNode, "left", currentNode.getDepth() + 1, currentNode.getCost(), currentNode.getStar(), currentNode.getFlower())
                left = son.leftMovement(tomPos)
                son.setNewCost(left)
                son.setTomPos(left)
                son.moveLeft(tomPos)
                if son.compareCicles2(left):
                    stack.append(son)  # اضافه کردن به انتهای استک
                    if son.getDepth() > depth:
                        depth = son.getDepth()

            # بررسی حرکت به سمت پایین
            if tomPos[0] + 1 < self.height_world and currentNode.getState()[tomPos[0] + 1, tomPos[1]] != 1:
                son = Node(currentNode.getState(), currentNode, "down", currentNode.getDepth() + 1, currentNode.getCost(), currentNode.getStar(), currentNode.getFlower())
                down = son.downMovement(tomPos)
                son.setNewCost(down)
                son.setTomPos(down)
                son.moveDown(tomPos)
                if son.compareCicles2(down):
                    stack.append(son)
                    if son.getDepth() > depth:
                        depth = son.getDepth()

            # بررسی حرکت به سمت بالا
            if tomPos[0] - 1 >= 0 and currentNode.getState()[tomPos[0] - 1, tomPos[1]] != 1:
                son = Node(currentNode.getState(), currentNode, "up", currentNode.getDepth() + 1, currentNode.getCost(), currentNode.getStar(), currentNode.getFlower())
                up = son.upMovement(tomPos)
                son.setNewCost(up)
                son.setTomPos(up)
                son.moveUp(tomPos)
                if son.compareCicles2(up):
                    stack.append(son)
                    if son.getDepth() > depth:
                        depth = son.getDepth()




        elapsedTime = process_time() - startTime
        elapsedTimeFormatted = "%.10f s." % elapsedTime
        self.setComputingTime(elapsedTimeFormatted)

        solution = currentNode.recreateSolutionWorld()
        solutionWorld = solution[::-1]
        print("Expanded nodes: ", expandedNodes+1)  # Good
        print("Depth: ", depth)
        print(" final cost of the solution is: " + str(currentNode.getCost()))
        print(currentNode.recreateSolution())
        return [solutionWorld, expandedNodes + 1, depth]