from node import Node
from time import process_time


class StarAlgorithm:
    def __init__(self, world):
        self.emptyNode = Node(None, None, "first father", -1, 0, 0, 0)
        self.firstNode = Node(world, self.emptyNode, " ", 0, 0, 0, 0) 
        self.tomPos = self.firstNode.searchForTom()
        self.jerryPos = self.searchForJerry(world) #پیدا کردن موقعیت جری و ذخیره کردن ان
        self.stack = [self.firstNode]
        self.computingTime = ""
        self.length_world = world.shape[0]
        self.height_world = world.shape[1]

    #از  نود های موجود در استک ، اونی رو انتخاب میکنه که 
    #کمترین مقدار مجموع هزینه و هوریستیک را داشته باشد
    def getNodeMinSumCostHeuristic(self, stack):
        minNode = min(stack, key=lambda node: node.getSumCostHeuristic())
        return minNode

    #برگرداندن زمان کل اجرای الگوریتم 
    def getComputingTime(self):
        return self.computingTime

    #ذخیره کردن زمان اجرای الگوریتم 
    def setComputingTime(self, computingTime):
        self.computingTime = computingTime

    def searchForJerry(self, world):
        jerryPos = []
        for i in range(world.shape[0]):
            for j in range(world.shape[1]):
                if (world[i, j] == self.firstNode.PRINCESS):
                    jerryPos.append(i)
                    jerryPos.append(j)
        return jerryPos

    #پیاده سازی الگوریتم A-Star 
    def start(self):
        startTime = process_time()
        stack = self.stack
        tomPos = self.tomPos
        expandedNodes = 0
        depth = 0

         #TO DO : define currentNode
        #انتخاب گره فعلی از استک با استفاده از تابع مربوطه 
        currentNode = self.getNodeMinSumCostHeuristic(stack)

        #حذف ان گره از استک تا دوباره پردازش نشود
        stack.remove(currentNode)
        

        while not (currentNode.isGoal()):
           


            if (not (tomPos[1]+1 >= self.length_world) and currentNode.getState()[tomPos[0], tomPos[1]+1] != 1):
                son = Node(currentNode.getState(), currentNode,
                           "right", currentNode.getDepth() + 1, currentNode.getCost(), currentNode.getStar(), currentNode.getFlower())

                right = son.rightMovement(tomPos)
                son.setNewCost(right)
                son.setTomPos(right)

            
                # TO DO: implement the heuristic logic for moving right
                manhattanDistance = son.calculateManhattanDistance(self.jerryPos)
                heuristic = son.calculateHeuristic(manhattanDistance)
                son.setHeuristic(heuristic)
                son.setSumCostHeuristic(son.getCost() + heuristic)


                son.moveRight(tomPos)
                if (son.avoidGoBack2(right)):
                    stack.append(son)
                    if (son.getDepth() > depth):
                        depth = son.getDepth()


            # Check if left side is free
            if (not (tomPos[1]-1 < 0) and currentNode.getState()[tomPos[0], tomPos[1]-1] != 1):
                son = Node(currentNode.getState(), currentNode,
                           "left", currentNode.getDepth() + 1, currentNode.getCost(), currentNode.getStar(), currentNode.getFlower())

                left = son.leftMovement(tomPos)
                son.setNewCost(left)
                son.setTomPos(left)


                # TO DO: implement the heuristic logic for left
               
                manhattanDistance = son.calculateManhattanDistance(self.jerryPos)
                heuristic = son.calculateHeuristic(manhattanDistance)
                son.setHeuristic(heuristic)
                son.setSumCostHeuristic(son.getCost() + heuristic)


                son.moveLeft(tomPos)
                if (son.avoidGoBack2(left)):
                    stack.append(son)
                    if (son.getDepth() > depth):
                        depth = son.getDepth()



            # Check if down-side is free
            if (not (tomPos[0]+1 >= self.height_world) and currentNode.getState()[tomPos[0]+1, tomPos[1]] != 1):
                son = Node(currentNode.getState(), currentNode,
                           "down", currentNode.getDepth() + 1, currentNode.getCost(), currentNode.getStar(), currentNode.getFlower())

                down = son.downMovement(tomPos)
                son.setNewCost(down)
                son.setTomPos(down)

                # TO DO: implement the heuristic logic for moving down
                manhattanDstance = son.calculateManhattanDistance(self.jerryPos)
                heuristic = son.calculateHeuristic(manhattanDistance)
                son.setHeuristic(heuristic)
                son.setSumCostHeuristic(son.getCost() + heuristic)

                son.moveDown(tomPos)
                if (son.avoidGoBack2(down)):
                    stack.append(son)
                    if (son.getDepth() > depth):
                        depth = son.getDepth()


            # Check if up-side is free
            if (not (tomPos[0]-1 < 0) and currentNode.getState()[tomPos[0]-1, tomPos[1]] != 1):
                son = Node(currentNode.getState(), currentNode,
                           "up", currentNode.getDepth() + 1, currentNode.getCost(), currentNode.getStar(), currentNode.getFlower())

                up = son.upMovement(tomPos)
                son.setNewCost(up)
                son.setTomPos(up)

                # TO DO: implement the heuristic logic for moving up
                
                manhattanDistance = son.calculateManhattanDistance(self.jerryPos)
                heuristic = son.calculateHeuristic(manhattanDistance)
                son.setHeuristic(heuristic)
                son.setSumCostHeuristic(son.getCost() + heuristic)


                son.moveUp(tomPos)
                if (son.avoidGoBack2(up)):
                    stack.append(son)
                    if (son.getDepth() > depth):
                        depth = son.getDepth()

            # TO DO : Update the stack
            # The stack is updated automatically in each movement check (right, left, up, down)
            # But after every move, you may want to re-check and sort the stack based on the heuristic
            # با استفاده از تابع مربوطه ،استک  مرتب میشود تا نود هایی  که کمترین هزینه را دارند زودتر بررسی شوند 
            currentNode = self.getNodeMinSumCostHeuristic(stack)
            stack.remove(currentNode)

            expandedNodes += 1
            tomPos = currentNode.getTomPos()



        elapsedTime = process_time() - startTime
        elapsedTimeFormatted = "%.10f s." % elapsedTime
        self.setComputingTime(elapsedTimeFormatted)

        solution = currentNode.recreateSolutionWorld()
        solutionWorld = solution[::-1]
        print("Expanded nodes: ", expandedNodes+1)  # Good
        print("Depth: ", depth)
        print("The final cost of the solution is: " + str(currentNode.getCost()))
        print(currentNode.recreateSolution())
        return [solutionWorld, expandedNodes+1, depth]
