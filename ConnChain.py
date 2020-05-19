import pandas as pd
import random
import time

"""
Generate Connections for each - Layer 1 - X
Intermingle Connections
Randomly check if infected if parent infected
"""
start_time = time.time()

Nodes = 6
Layers = 6
InfecRt = 0.5

data = {'parent': [0], 'id':[0], 'infect': [0], 'layer':[0]}
df = pd.DataFrame(data=data)

#--------- create population ----------
calc=0
cnum=0
par=-1
for lyr in range(1,Layers+1):
    pval = pow(Nodes,lyr)
    calc = calc + pval
    
    for n in range(1, pval+1):
        if ((cnum % Nodes)==0):
            par = par + 1
        cnum=cnum+1

        data = {'parent': [par], 'id':[cnum], 'infect': [0], 'layer':[lyr]}
        tmpdf = pd.DataFrame(data=data)
        
        df = pd.concat([df, tmpdf])
#-- endfor --
totpop = df.shape[0]


df['me'] = df['id']
df.set_index(['id'])

#add for audit trail
df['log_rnd'] = 0
df['log_par'] = 0
df['wave'] = 0

#-------- run simulation 1 time(s) with X Waves -------
#ttlwaves = how many infected people join the population
#Take it layer by layer, roll the dice x times/waves
#then for those infected  keep rolling for each children
#as ppl in reality are more intermingle I would keep the top-down model 
#the same but concatenate more rows at the bottom of the dataframe
#to test increased complexity
ttlwaves = 100
for wave in range(1,ttlwaves+1):
    for lyr in range(1,Layers+1):
        for id in df[(df['layer']==lyr) & (df['infect']==0)]['id']:
            par = df[df['id']==id]['parent'].iloc[0]     #parent value
            isinf = df[df['id']==par]['infect'].iloc[0]   #parent is infected value
            wvinf = df[df['id']==par]['wave'].iloc[0]     #parent is infected value wave
         
            r = 0
            if ((isinf==1 and wvinf==wave) or (lyr <= 1)):
                r = random.random()
          
            if (r >= InfecRt):
                df.iloc[id,2] = 1            #set as infected
                df.iloc[id,7] = wave         #set wave
                df.iloc[id,5] = r            #log random num
                df.iloc[id,6] = par          #log parent value

elaps = round((time.time() - start_time)/60,2)

#save workings
df.to_csv('Data\\connchain.csv')
