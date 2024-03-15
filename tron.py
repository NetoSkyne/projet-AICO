import sys
import math

#depth setting
DEPTH = 4
#liste des cases occupees
occupied_spaces =[]

#distance manhattan
def distance(a,b):
    x1, y1 = a
    x2, y2 = b
    return(abs(x1-x2)+abs(y1-y2))



#recherche cases voisines libres
def openNeighbours(a, occupied_spaces):
    neighbours  = []
    x, y        = a
    if x > 0:
        neighbours.append((x-1, y))
    if x < 29:
        neighbours.append((x+1, y))
    if y > 0:
        neighbours.append((x, y-1))
    if y < 19:
        neighbours.append((x, y+1))


    neighbours = list(filter(lambda i: i not in occupied_spaces, neighbours))
    return neighbours

#heuristique simple degre liberte
def possibleMovesHeuristic(player, opponent, occupied_spaces):
    player_directions   = len(openNeighbours(player, occupied_spaces))
    opponent_directions = len(openNeighbours(opponent, occupied_spaces))
    return(player_directions - opponent_directions)
    
#heuristique distance aux murs
def wallDistanceHeuristic(player, opponent, occupied_spaces):
    player_wall_distance = 0
    opponent_wall_distance = 0
    for wall in occupied_spaces:
        player_wall_distance += distance(player,wall)
        opponent_wall_distance += distance(opponent,wall)
    return len(occupied_spaces)/(player_wall_distance )

#calcul direction
def nextMove(current, next):
    x1, y1 = current
    x2, y2 = next
    if x1 > x2:
        return "LEFT"
    if x1 < x2:
        return "RIGHT"
    if y1 > y2:
        return "UP"
    return "DOWN"

def minimax(depth, player, opponent, occupied_spaces, isMax):
    """
        Permet de calculet les scores des branches de l'arbre recursivement
        Combine actuellement deux heuristiques simples pour l'evaluation des scores
        depth: profondeur de l'arbre
        
        isMax: bool permettant de traiter les cas de minimisation et maximisation
    """
    #TODO Alpha-Beta
    
    possible_directions = openNeighbours(player, occupied_spaces)
    
    #gameover check
    if not possible_directions:
        print("cinquante", file=sys.stderr, flush=True) 
        if isMax:
            return -50, player #penalite
        else:
            return 50, player
          
    scores = []
    for node in possible_directions:
        
        if depth == 0: #fin de recursion
            score = wallDistanceHeuristic(player, opponent, occupied_spaces) + possibleMovesHeuristic(player, opponent, occupied_spaces)
            if not isMax:
                score =  -score
        
        else:
            if isMax:
                score, _ = minimax(depth-1, opponent,node,  occupied_spaces + [node], False)
            else:
                score, _ = minimax(depth-1,  opponent,node,occupied_spaces + [node], True)
        
        scores.append(score)
         
    if isMax:
        return max(scores), possible_directions[scores.index(max(scores))]
    else:
        return min(scores), possible_directions[scores.index(min(scores))]
        
# game loop
while True:
    # n: total number of players (2 to 4).
    # p: your player number (0 to 3).
    n, p = [int(i) for i in input().split()]
    player = (0,0)
    opponent = (0,0)
    for i in range(n):
        # x0: starting X coordinate of lightcycle (or -1)
        # y0: starting Y coordinate of lightcycle (or -1)
        # x1: starting X coordinate of lightcycle (can be the same as X0 if you play before this player)
        # y1: starting Y coordinate of lightcycle (can be the same as Y0 if you play before this player)
        x0, y0, x1, y1  = [int(j) for j in input().split()]
        
        #remplissage des cases occupees
        occupied_spaces.append((x1, y1))
        if i == p:
            player = (x1, y1)
        else:
            opponent = (x1, y1)

    scores, next_position = minimax(DEPTH ,player, opponent, occupied_spaces,True)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    
    # A single line with UP, DOWN, LEFT or RIGHT
    print(nextMove(player,next_position))

    #print(scores, next_position, file=sys.stderr, flush=True)




