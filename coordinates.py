import random

def create_nodes(amount):
    points = []
    for _ in range(amount):
        x = random.randrange(585, 1250)
        y = random.randrange(80, 745)
        
        while True:
            if x <= 1025 and y <= 195:
                x = random.randrange(585, 1250)
                y = random.randrange(80, 745)
            elif x <= 785 and y <= 230:
                x = random.randrange(585, 1250)
                y = random.randrange(80, 745)
            elif x <= 745 and y <= 240:
                x = random.randrange(585, 1250)
                y = random.randrange(80, 745)
            elif 890 <= x <= 970 and 190 <= y <= 250:
                x = random.randrange(585, 1250)
                y = random.randrange(80, 745)
            elif 785 <= x <= 890 and 190 <= y <= 220:
                x = random.randrange(585, 1250)
                y = random.randrange(80, 745)
            else:
                break

        point = x, y      
        points.append(point)
    return points