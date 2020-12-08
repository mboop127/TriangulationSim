#this code is intentionally inefficient as it is built to be readable

import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

size = 10000 #voterbase size
center = 0 #starting political center
deviation = 3 #starting ideological deviation
LeftPosition = 1 #starting ideology of left party, must always be greater than right position
RightPosition = -2 #starting ideology of right party
ElectionGravity = .1 #shift in population's ideology toward party positions during election
LeftWinGravity = .05 #shift in population's ideology toward left party positions after win
RightWinGravity = .05 #shift in population's ideology toward right party positions after win
randomness = .1 #changes weight of randomness in each election
Shift = 0 #shift in ideology over time
TriangulationShift = .11

elections = 21 #controls how many elections
trials = 1 # controls how many trials

#stuff for plotting
Lwin = []
Lwin2 = []
Rwin = []
Rwin2 = []
meanideology = []
Xaxis = []
LeftPositionList = []
RightPositionList = []

for runs in range(trials):

    #generate voterbase
    pop = []
    for i in range(size):
        pop.append(random.normalvariate(center,deviation))

    for cycle in range(elections):

        #triangulation (shifts party/ies to center)
        if LeftPosition > (sum(pop)/len(pop)):
            LeftPosition = LeftPosition - TriangulationShift
        elif LeftPostition < (sum(pop)/len(pop)):
            LeftPosition = LeftPosition + TriangulationShift

        #if RightPosition < (sum(pop)/len(pop)):
        #    RightPosition = RightPosition + TriangulationShift
        #elif RightPosition > (sum(pop)/len(pop)):
        #    RightPosition = RightPosition - TriangulationShift

        #shift calc (natural ideological shift)
        for i in range(len(pop)):
            pop[i] = pop[i] + Shift*cycle

        #election gravity calc (population ideology shifts according to campaigns)
        for i in range(len(pop)):
            pop[i] = pop[i] + (ElectionGravity * LeftPosition) + (ElectionGravity * RightPosition)


        #election
        rvotes = 0
        for i in range(len(pop)):
            left = abs(pop[i] - LeftPosition) + randomness * random.random() #measures ideological difference from the left
            right = abs(pop[i] - RightPosition) + randomness * random.random() #measures ideological difference from the right
            if right < left:
                rvotes = rvotes + 1

        if rvotes > len(pop)/2:
            #win gravity (models that each party uses its wins to shift the public towards the right/left)
            for i in range(len(pop)):
                pop[i] = pop[i] + (RightWinGravity * RightPosition)

            #plot stuff
            Rwin.append(100)
            Rwin2.append(-100)
            Lwin.append(0)
            Lwin2.append(0)

        else:
            #win gravity (models that each party uses its wins to shift the public towards the right/left)
            for i in range(len(pop)):
                pop[i] = pop[i] + (LeftWinGravity * LeftPosition)

            #plot stuff
            Rwin.append(0)
            Rwin2.append(0)
            Lwin.append(100)
            Lwin2.append(-100)

        meanideology.append(sum(pop)/len(pop))
        Xaxis.append(cycle)
        LeftPositionList.append(LeftPostition)
        RightPositionList.append(RightPosition)


#plots ideology
plt.suptitle("Mean Ideology Over Time",fontsize = 18)
plt.title("(left party triangulating)",fontsize = 12)
plt.xlabel("Number of Election Cycles",fontsize = 14)
plt.ylabel("Average Voter Ideology",fontsize = 14)
#plats bars
plt.bar(Xaxis,Lwin,color='b',alpha = .2,width = 1)
plt.bar(Xaxis,Rwin,color='r',alpha = .2,width = 1)
plt.bar(Xaxis,Lwin2,color='b',alpha = .2,width = 1)
plt.bar(Xaxis,Rwin2,color='r',alpha = .2,width = 1)
#plt.scatter(Xaxis, meanideology, color = 'black') #scatter
plt.plot(Xaxis, meanideology, color = 'black') #line
plt.plot(Xaxis,LeftPositionList,'--',color='b')
plt.plot(Xaxis,RightPositionList,'--',color='r')
plt.xticks([0,5,10,15,20])
plt.yticks([-5,0,5], ('Right','Center','Left'),fontsize = 10)
plt.xlim((0, elections-1))
plt.ylim((-5, 5))
plt.text(.24, 3.66, 'Election gravity = ' + str(ElectionGravity) + '\nLeft win gravity = ' + str(LeftWinGravity) + '\nRight win gravity = ' + str(RightWinGravity),bbox=dict(facecolor='white', edgecolor='black'))
red_patch = mpatches.Patch(color='red', label='Right Party Position')
blue_patch = mpatches.Patch(color='blue', label='Left Party Position')
black_patch = mpatches.Patch(color='black', label='Average Voter Ideology')
plt.legend(handles=[blue_patch,red_patch],loc='upper right')
plt.show()
