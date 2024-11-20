# search.py stores minimax and heuristic alpha-beta pruning (up to user depth d, possible infinite) algorithms
from functions import *
from L_game import *

class miniMax(Player):
    
    def getMove(self, gameState):
        value, move = self.getValue(gameState, 0, 0)
        return move
    
    def getvalue(self, gameState, d, agentIndex):
        if (d == self.depth or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState), None
    
        numAgents = gameState.getNumAgents()
        legalMoves = gameState.getLegalMoves(agentIndex)

        if agentIndex == 0:
            bestScore = float(-'inf')
            bestMove = None
        
            for move in legalMoves:
                successor = gameState.generateSuccessor(agentIndex, move)
                value, _ = self.getValue(successor, d+1 if (agentIndex+1) % numAgents == 0 else d, (agentIndex+1) % numAgents)
                if value > bestScore:
                    bestScore = value
                    bestMove = move
            return bestScore, bestMove
        
        else:
            bestScore = float('inf')
            bestMove = None 

            for action in legalMoves:
                successor = gameState.generateSuccessor(agentIndex, move)
                value, _ = self.getValue(successor, d+1 if (agentIndex+1) % numAgents == 0 else d, (agentIndex+1) % numAgents)
                if value < bestScore:
                    bestScore = value
                    bestMove = move
            return bestScore, bestMove
    
class AlphaBetaAgent(Player):
    def getMove(self, gameState):
        numAgent = gameState.getNumAgents()
        moveScore = []

        def stopRM(list):
            return [x for x in list if x != 'Stop']
        
        def alphaBeta(successor, counter, alpha, beta):
            if counter >= self.depth * numAgent or successor.isWin() or successor.isLose():
                return self.evaluationFunction(successor)
            
            if counter % numAgent != 0:
                result = float('inf')
                for num in stopRM(successor.getLegalMoves(counter % numAgent)):
                    dot = successor.generateSuccessor(counter % numAgent, num)
                    result = min(result, alphaBeta(dot, counter+1, alpha, beta))
                    beta = min(beta, result)

                    if beta < alpha:
                        break
                return result
            else:
                result = float(-'inf')
                for num in stopRM(successor.getLegalMoves(counter % numAgent)):
                    dot = successor.generateSuccessor(counter % numAgent, num)
                    result = max(result, alphaBeta(dot, counter+1, alpha, beta))
                    alpha = max(alpha, result)

                    if counter == 0:
                        moveScore.append(result)

                    if beta < alpha:
                        break
                return result
        
        result = alphaBeta(gameState, 0, float(-'inf'), float('inf'))
        return stopRM(gameState.getLegalMoves(0))[moveScore.index(max(moveScore))]
