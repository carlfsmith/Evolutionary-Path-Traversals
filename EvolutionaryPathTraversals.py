'''
Created on Feb 20, 2015

@author: Carl
'''
from __future__ import print_function
from PIL import Image
import time
import random
import math
#import xlsxwriter

def propegate(population, cost):
    fighters = []
    fight_prob = []
    #begin tournament..
    fighters.append(random.randint(0,len(population)-1))
    fighters.append(random.randint(0,len(population)-1))
    probability_spread = 0.999     #makes higher probabilities higher and lower probabilities lower; normally 0.999
    kill_chrome = -1
    while fighters[0] == fighters[1]:
        fighters[1] = random.randint(0,len(population)-1)
    d = -1
    if cost[fighters[0]] == cost[fighters[1]]:
        fight_prob = [0.5,0.5]
    else:
        m = min([cost[fighters[0]], cost[fighters[1]]]) * probability_spread
        d = (cost[fighters[0]] + cost[fighters[1]] - 2*m)   #give fighter 0 an increased chance of winning
        fight_prob = [(d-(cost[fighters[0]]-m))/d, (d-(cost[fighters[1]]-m))/d]
    r = random.random()
    i = 0
    while True:
        if i == 2:
            i = 0
        if r < fight_prob[i]:
            if i == 0:
                kill_chrome = fighters[1]
            else:
                kill_chrome = fighters[0]
            break
        else:
            r-=fight_prob[i]
        i+=1
    del cost[kill_chrome]
    del population[kill_chrome]
    #determining cross-over..
        #find cross pair
    r = random.random()
    cross_pair = []
    s = sum(cost)                   #determine sum to maintain ratios of probabilities summing to 1
    probability = [(s - c) for c in cost]
    m = min(probability) * probability_spread    #get most of the value of the min number
    probability = [(p - m) for p in probability]
    s2 = sum(probability)
    probability = [(p / s2) for p in probability]
    r = random.random()
    i = 0
    while True:
        if len(cross_pair) == 2:
            break
        elif i == len(population):
            i = 0
        if r < probability[i]:
            cross_pair.append(i)
        else:
            r -= probability[i]
        i+=1
        #create child chromosome
    cut = -1          
    chromosome = []               #initialize index to cut
    mother_size = len(population[cross_pair[0]])
    father_size = len(population[cross_pair[1]]) 
    if len(population[cross_pair[0]]) == 0 and len(population[cross_pair[1]]) == 0:
        pass
    elif mother_size == 0:
        cut = random.randint(0, father_size-1)
        chromosome.extend(population[cross_pair[1]][cut:father_size])
    elif father_size == 0:
        cut = random.randint(0, mother_size-1)
        chromosome.extend(population[cross_pair[0]][0:cut+1])
    elif mother_size <= father_size:    #determine where to cut by finding the smallest chromosome
        cut = random.randint(0, mother_size-1)
        chromosome.extend(population[cross_pair[0]][0:cut+1])                 
        chromosome.extend(population[cross_pair[1]][cut+1:father_size])            #append second half of genes to new chromosome                     #append first half of genes to new chromosome
    elif mother_size > father_size:
        cut = random.randint(0, father_size-1)
        chromosome.extend(population[cross_pair[0]][0:cut+1])                 
        chromosome.extend(population[cross_pair[1]][cut+1:father_size])            #append second half of genes to new chromosome                   #append first half of genes to new chromosome
    population.append(chromosome)
    #add random gene to randomly selected chromosome
    MAX_STEPS = 25         #normally 20-40
    add_gene(population, MAX_STEPS)
    #drop a random gene from a randomly selected chromosome
    drop_gene(population)
    #mutate a random angle in a random chromosome
    mutate_angle(population)
    #mutate a step count in a random chromosome
    mutate_step(population, MAX_STEPS) 
     
def add_gene(population, MAX_STEPS):      
    rC = random.randint(0, len(population)-1)
    angle = 2.0 * math.pi * random.random()
    steps = random.randint(1, MAX_STEPS)
    gene = (angle,steps)
    if len(population[rC]) > 0:
        rG = random.randint(0, len(population[rC])-1)
        population[rC].insert(rG, gene) 
    else:
        population[rC].append(gene)

def drop_gene(population):
    rC = random.randint(0, len(population)-1)
    if len(population[rC]) > 0:
        rG = random.randint(0, len(population[rC])-1)
        del population[rC][rG]
   
def mutate_angle(population):
    rC = random.randint(0, len(population)-1)
    if len(population[rC]) > 0:
        rG = random.randint(0, len(population[rC])-1)
        angle = 2.0 * math.pi * random.random()
        population[rC][rG] = (angle,population[rC][rG][1]) 
     
def mutate_step(population, MAX_STEPS):
    rC = random.randint(0, len(population)-1)
    if len(population[rC]) > 0:
        rG = random.randint(0, len(population[rC])-1)
        steps = random.randint(1, MAX_STEPS)
        population[rC][rG] = (population[rC][rG][0],steps)
         
def calc_fitness(start, goal, border, population, pixels):
    cost = [0.0 for x in range(len(population))]
    xG,yG = goal
    i = 0
    for chromosome in population:
        x,y = start
        for gene in chromosome:
            if gene is None:
                angle,steps = 0.0, 0
            else:
                angle,steps = gene
            for j in range(1,steps):
                x,y = x + math.cos(angle), y + math.sin(angle)
                x_flr,y_flr = math.floor(x), math.floor(y)
                if x_flr >= 0 and x_flr < border[0] and y_flr >= 0 and y_flr < border[1]:        #if the position is not out of bounds
                    cost[i] += pixels[math.floor(x), math.floor(y)][1]
                else:
                    cost[i] += 255*100            #make the cost impossibly high (255 is max green value)
        cost[i] += 500 * (math.sqrt((xG-x)**2 + (yG-y)**2))
        i+=1
    return cost

def trace_population(image, start, population):
    change = 1
    for chromosome in population:
        if change == 31:
            change = 0
        x,y = start
        pixels = image.load()
        border = image.size
        X = math.floor(255 * change/5)
        if change >= 1 and change < 6:
            color = (X,0,0)
        elif change >= 6 and change < 11:
            color = (0,X,0)
        elif change >= 11 and change < 16:
            color = (0,0,X)
        elif change >= 16 and change < 21:
            color = (X,X,0)
        elif change >= 21 and change < 26:
            color = (X,0,X)
        elif change >= 26 and change < 31:
            color = (0,X,X)
        pixels[x,y] = color
        for gene in chromosome:
            if gene is None:
                angle,steps = 0.0, 0
            else:
                angle,steps = gene
            for j in range(1,steps):
                x,y = x + math.cos(angle), y + math.sin(angle)
                x_flr,y_flr = math.floor(x), math.floor(y)
                if x_flr >= 0 and x_flr < border[0] and y_flr >= 0 and y_flr < border[1]:        #if the position is not out of bounds
                    pixels[x_flr,y_flr] = color
        change+=1
    #image.show()
    image.save("population.png")

def trace_path(image, start, population, cost):
    min_cost = min(cost)
    local_min = -1
    for i in range (0,len(cost)):
        if cost[i] == min_cost:
            local_min = i
            break
    color = (0,255,0)
    x,y = start
    pixels = image.load()
    border = image.size
    pixels[x,y] = color
    for gene in population[local_min]:
        if gene is None:
            angle,steps = 0.0, 0
        else:
            angle,steps = gene
        for j in range(1,steps):
            x,y = x + math.cos(angle), y + math.sin(angle)
            x_flr,y_flr = math.floor(x), math.floor(y)
            if x_flr >= 0 and x_flr < border[0] and y_flr >= 0 and y_flr < border[1]:        #if the position is not out of bounds
                pixels[x_flr,y_flr] = color
    #image.show()
    image.save("path.png")

def draw_graph(min_costs):
    workbook = xlsxwriter.Workbook('chart_line.xlsx')
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': 1})
    headings = ['Number', 'Cost']
    times = [(str(math.floor(t*10 / 60)) + "." + str(t*10 % 60)) for t in range(len(min_costs))]
    worksheet.write_row('A1', headings, bold)
    worksheet.write_column('A2', times)
    worksheet.write_column('B2', min_costs)
    # Create a new chart object. In this case an embedded chart.
    chart = workbook.add_chart({'type': 'line'})
    # Configure series.
    chart.add_series({
        'name':       '=Sheet1!$B$1',
        'categories': '=Sheet1!$A$2:$A$'+str(len(times)+1),
        'values':     '=Sheet1!$B$2:$B$'+str(len(times)+1),
        'line':       {'color': '#FF9900'},
    })
    # Add a chart title and some axis labels.
    chart.set_title ({'name': 'Cost of Genetic Algorithm Over Time'})
    chart.set_x_axis({'name': 'Time(m.s)'})
    chart.set_y_axis({'name': 'Cost'}) 
    chart.set_y_axis({'interval_unit': 25000})
    # Set an Excel chart style. Colors with white outline and shadow.
    chart.set_style(10)
    # Insert the chart into the worksheet (with an offset).
    worksheet.insert_chart('D2', chart, {'x_offset': 25, 'y_offset': 10}) 
    workbook.close()

def genetic_algo(start, goal, image, min_costs):
    pixels = image.load()
    population = [[] for x in range(60)]
    x,y = image.size
    border = (x,y)
    it = 0
    st = time.clock()
    first_zero = True
    interval = 10    #seconds
    while True:
        cost = calc_fitness(start, goal, border, population, pixels)
        propegate(population, cost)
        it+=1
        elapsed = math.floor((time.clock() - st))
        if elapsed % interval == 0 and first_zero:
            m, s = divmod(elapsed, 60)
            min_costs.append(min(cost))
            first_zero = False
            print("time:  ",m,".",s,", \tgeneration:  ",it,", \tmin_cost:  ",min(cost),sep="")
        elif elapsed % interval != 0 and not first_zero:
            first_zero = True
        elif elapsed > 5*60:
            #print image of costs at regular intervals..
#             img = Image.open('terrain.png')
#             if image.mode != 'RGB':
#                 image= image.convert('RGB')
#             trace_population(img, start, population)
            return population, cost

if __name__ == '__main__':
    start = (100,100)
    goal = (400,400)
    min_costs = []
    image = Image.open('terrain.png')
    if image.mode != 'RGB':
        image = image.convert('RGB')
    population, cost = genetic_algo(start, goal, image, min_costs)
    #draw_graph(min_costs)
#     #draw the path
#     trace_path(image, start, population, cost)
#     #draw the population
#     image = Image.open('terrain.png')
#     if image.mode != 'RGB':
#         image = image.convert('RGB')
#     trace_population(image, start, population)