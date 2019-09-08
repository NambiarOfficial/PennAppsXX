activityM={'Athlete':52,'Excellent':57.5,'Good':63.5,'Above Average':67.5,'Average':71.5,
          'Below Average':77.5,'Poor':82}
activityM2={'Athlete':51.5,'Excellent':58,'Good':63.5,'Above Average':68,'Average':72.5,
          'Below Average':78,'Poor':82}
activityM3={'Athlete':58,'Excellent':59.5,'Good':64.5,'Above Average':68,
            'Average':73,'Below Average':79,'Poor':83}
activityM4={'Athlete':58.5,'Excellent':60.5,'Good':65.5,'Above Average':69.5,
            'Average':74.5,'Below Average':80,'Poor':84}
activityM5={'Athlete':53.5,'Excellent':59,'Good':63.5,'Above Average':67.5,
            'Average':72.5,'Below Average':76.5,'Poor':80}
activityM6={'Athlete':52.5,'Excellent':58.5,'Good':63.5,
            'Above Average':67.5,
            'Average':71.5,'Below Average':76.5,'Poor':80}

activityF={'Athlete':57,'Excellent':63,'Good':67.5,
           'Above Average':71.5,'Average':76,'Below Average':81.5,
           'Poor':85}
activityF2={'Athlete':56.5,'Excellent':62,'Good':66.5,'Above Average':70.5,
            'Average':72.5,
          'Below Average':74.5,'Poor':83}
activityF3={'Athlete':56.5,'Excellent':62,'Good':67,'Above Average':71.5,
            'Average':73,'Below Average':79,'Poor':85}
activityF4={'Athlete':57,'Excellent':63,'Good':67.5,
            'Above Average':71.5,
            'Average':56.5,'Below Average':80.5,'Poor':84}
activityF5={'Athlete':56.5,'Excellent':62,'Good':66.5,'Above Average':71,
            'Average':72.5,'Below Average':80.5,'Poor':84}
activityF6={'Athlete':56.5,'Excellent':62,'Good':66.5,'Above Average':70.5,
            'Average':74.5,'Below Average':80.5,'Poor':84}
#1: male 0: Female Ladkiya jhooth hi hai bc
def appropriate_H_R(gender,age,reading):
    if gender:
        if age>=18 and age<=25:
            if reading<=activityM['Athlete']:
                fitness_level='Athlete'
            elif reading>activityM['Athlete'] and reading<=activityM['Excellent']:
                fitness_level='Excellent'
            elif reading>activityM['Excellent'] and reading<=activityM['Good']:
                fitness_level='Good'
            elif reading>activityM['Good'] and reading<=activityM['Above Average']:
                fitness_level='Above Average'
            elif reading>activityM['Above Average'] and reading<=activityM['Average']:
                fitness_level='Average'
            elif reading>activityM['Average'] and reading<=activityM['Below Average']:
                fitness_level='Below Average'
            elif reading>activityM['Below Average'] and reading<=activityM['Poor']:
                fitness_level='Poor'
        if age>25 and age<=35:
            #print('here')
            #print(activityM2['Excellent'],activityM2['Athlete'])
            #print(reading)
            if reading<=activityM2['Athlete']:
                fitness_level='Athlete'
            elif reading>activityM2['Athlete'] and reading<=activityM2['Excellent']:
                #print('hhhere')
                fitness_level='Excellent'
            elif reading>activityM2['Excellent'] and reading<=activityM2['Good']:
                
                #print('here')
                fitness_level='Good'
            elif reading>activityM2['Good'] and reading<=activityM2['Above Average']:
                fitness_level='Above Average'
            elif reading>activityM2['Above Average'] and reading<=activityM2['Average']:
                fitness_level='Average'
            elif reading>activityM2['Average'] and reading<=activityM2['Below Average']:
                fitness_level='Below Average'
            elif reading>activityM2['Below Average'] and reading<=activityM2['Poor']:
                fitness_level='Poor'
        if age>35 and age<=45:
            if reading<=activityM3['Athlete']:
                fitness_level='Athlete'
            elif reading>activityM3['Athlete'] and reading<=activityM3['Excellent']:
                fitness_level='Excellent'
            elif reading>activityM3['Excellent'] and reading<=activityM3['Good']:
                fitness_level='Good'
            elif reading>activityM3['Good'] and reading<=activityM3['Above Average']:
                fitness_level='Above Average'
            elif reading>activityM3['Above Average'] and reading<=activityM3['Average']:
                fitness_level='Average'
            elif reading>activityM3['Average'] and reading<=activityM3['Below Average']:
                fitness_level='Below Average'
            elif reading>activityM3['Below Average'] and reading<=activityM3['Poor']:
                fitness_level='Poor'
        if age>55 and age<=65:
            if reading<=activityM4['Athlete']:
                fitness_level='Athlete'
            elif reading>activityM4['Athlete'] and reading<=activityM4['Excellent']:
                fitness_level='Excellent'
            elif reading>activityM4['Excellent'] and reading<=activityM4['Good']:
                fitness_level='Good'
            elif reading>activityM4['Good'] and reading<=activityM4['Above Average']:
                fitness_level='Above Average'
            elif reading>activityM4['Above Average'] and reading<=activityM4['Average']:
                fitness_level='Average'
            elif reading>activityM4['Average'] and reading<=activityM4['Below Average']:
                fitness_level='Below Average'
            elif reading>activityM4['Below Average'] and reading<=activityM4['Poor']:
                fitness_level='Poor'
        if age>65 and age<=75:
            if reading<=activityM5['Athlete']:
                fitness_level='Athlete'
            elif reading>activityM5['Athlete'] and reading<=activityM5['Excellent']:
                fitness_level='Excellent'
            elif reading>activityM5['Excellent'] and reading<=activityM5['Good']:
                fitness_level='Good'
            elif reading>activityM5['Good'] and reading<=activityM5['Above Average']:
                fitness_level='Above Average'
            elif reading>activityM5['Above Average'] and reading<=activityM5['Average']:
                fitness_level='Average'
            elif reading>activityM5['Average'] and reading<=activityM5['Below Average']:
                fitness_level='Below Average'
            elif reading>activityM5['Below Average'] and reading<=activityM5['Poor']:
                fitness_level='Poor'
        if age>75:
            if reading<=activityM6['Athlete']:
                fitness_level='Athlete'
            elif reading>activityM6['Athlete'] and reading<=activityM6['Excellent']:
                fitness_level='Excellent'
            elif reading>activityM6['Excellent'] and reading<=activityM6['Good']:
                fitness_level='Good'
            elif reading>activityM6['Good'] and reading<=activityM6['Above Average']:
                fitness_level='Above Average'
            elif reading>activityM6['Above Average'] and reading<=activityM6['Average']:
                fitness_level='Average'
            elif reading>activityM6['Average'] and reading<=activityM6['Below Average']:
                fitness_level='Below Average'
            elif reading>activityM6['Below Average'] and reading<=activityM6['Poor']:
                fitness_level='Poor'
        return(fitness_level)
    else:
        if age>=18 and age<=25:
            if reading<=activityF['Athlete']:
                fitness_level='Athlete'
            elif reading>activityF['Athlete'] and reading<=activityF['Excellent']:
                fitness_level='Excellent'
            elif reading>activityF['Excellent'] and reading<=activityF['Good']:
                fitness_level='Good'
            elif reading>activityF['Good'] and reading<=activityF['Above Average']:
                fitness_level='Above Average'
            elif reading>activityF['Above Average'] and reading<=activityF['Average']:
                fitness_level='Average'
            elif reading>activityF['Average'] and reading<=activityF['Below Average']:
                fitness_level='Below Average'
            elif reading>activityF['Below Average'] and reading<=activityF['Poor']:
                fitness_level='Poor'
        if age>25 and age<=35:
            if reading<=activityF2['Athlete']:
                fitness_level='Athlete'
            elif reading>activityF2['Athlete'] and reading<=activityF2['Excellent']:
                fitness_level='Excellent'
            elif reading>activityF2['Excellent'] and reading<=activityF2['Good']:
                fitness_level='Good'
            elif reading>activityF2['Good'] and reading<=activityF2['Above Average']:
                fitness_level='Above Average'
            elif reading>activityF2['Above Average'] and reading<=activityF2['Average']:
                fitness_level='Average'
            elif reading>activityF2['Average'] and reading<=activityF2['Below Average']:
                fitness_level='Below Average'
            elif reading>activityF2['Below Average'] and reading<=activityF2['Poor']:
                fitness_level='Poor'
        if age>35 and age<=45:
            if reading<=activityF3['Athlete']:
                fitness_level='Athlete'
            elif reading>activityF3['Athlete'] and reading<=activityF3['Excellent']:
                fitness_level='Excellent'
            elif reading>activityF3['Excellent'] and reading<=activityF3['Good']:
                fitness_level='Good'
            elif reading>activityF3['Good'] and reading<=activityF3['Above Average']:
                fitness_level='Above Average'
            elif reading>activityF3['Above Average'] and reading<=activityF3['Average']:
                fitness_level='Average'
            elif reading>activityF3['Average'] and reading<=activityF3['Below Average']:
                fitness_level='Below Average'
            elif reading>activityF3['Below Average'] and reading<=activityF3['Poor']:
                fitness_level='Poor'
        if age>55 and age<=65:
            if reading<=activityF4['Athlete']:
                fitness_level='Athlete'
            elif reading>activityF4['Athlete'] and reading<=activityF4['Excellent']:
                fitness_level='Excellent'
            elif reading>activityF4['Excellent'] and reading<=activityF4['Good']:
                fitness_level='Good'
            elif reading>activityF4['Good'] and reading<=activityF4['Above Average']:
                fitness_level='Above Average'
            elif reading>activityF4['Above Average'] and reading<=activityF4['Average']:
                fitness_level='Average'
            elif reading>activityF4['Average'] and reading<=activityF4['Below Average']:
                fitness_level='Below Average'
            elif reading>activityF4['Below Average'] and reading<=activityF4['Poor']:
                fitness_level='Poor'
        if age>65 and age<=75:
            if reading<=activityF5['Athlete']:
                fitness_level='Athlete'
            elif reading>activityF5['Athlete'] and reading<=activityF5['Excellent']:
                fitness_level='Excellent'
            elif reading>activityF5['Excellent'] and reading<=activityF5['Good']:
                fitness_level='Good'
            elif reading>activityF5['Good'] and reading<=activityF5['Above Average']:
                fitness_level='Above Average'
            elif reading>activityF5['Above Average'] and reading<=activityF5['Average']:
                fitness_level='Average'
            elif reading>activityF5['Average'] and reading<=activityF5['Below Average']:
                fitness_level='Below Average'
            elif reading>activityF5['Below Average'] and reading<=activityF5['Poor']:
                fitness_level='Poor'
        if age>75:
            if reading<=activityF6['Athlete']:
                fitness_level='Athlete'
            elif reading>activityF6['Athlete'] and reading<=activityF6['Excellent']:
                fitness_level='Excellent'
            elif reading>activityF6['Excellent'] and reading<=activityF6['Good']:
                fitness_level='Good'
            elif reading>activityF6['Good'] and reading<=activityF6['Above Average']:
                fitness_level='Above Average'
            elif reading>activityF6['Above Average'] and reading<=activityF6['Average']:
                fitness_level='Average'
            elif reading>activityF6['Average'] and reading<=activityF6['Below Average']:
                fitness_level='Below Average'
            elif reading>activityF6['Below Average'] and reading<=activityF6['Poor']:
                fitness_level='Poor'
        return(fitness_level)

##x=appropriate_H_R(0,26,58)
##print(x)
import time
def count_heart_beats_per_minute(thresh=512):
    start=time.time()
    beats=0
    while time.time()-start<=60:
        val=getValue()
        if val>=thresh:
            beats+=1
    return(beats)
