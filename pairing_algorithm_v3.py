import random;

def group(theClass, isGenderImportant, isAbilityImportant, isPreferenceImportant):

    inOrderCandidatePool = theClass[:] ##this copy is the working list that will shrink
    candidatePool = []

    for i in range (len(inOrderCandidatePool)):
        rand = random.randint(0, len(inOrderCandidatePool) -1)
        candidatePool.append(inOrderCandidatePool[rand])
        inOrderCandidatePool.remove(inOrderCandidatePool[rand])
    newGroups = [] ##this is the current suggested groups list that will grow
    notGrouped = [] ##this stores ungrouped IDs for reference

    ## ~~~~FUTURE CODE~~~~ if isPreferenceConsidered == true: compare preference lists, check for identical matches,
        ##select a random student from the pool of remaining students each time in case 3 students chose eachother (DON'T look in the list sequentially)
        ##check recent history for the 2 people, if good, pair them in newGroups and remove them from candidatePool
        ##if all students were grouped, go on to finalizing groups, if not, randomize the rest

    ##sorting by gender
    males = []
    females = []
    others = []

    if isGenderImportant:    ##sort genders into the 3 gender lists each by ability level
        for person in candidatePool:
            if person[2] == 'male':
                males.append(person)
            elif person[2] == 'female':
                females.append(person)
            else:
                others.append(person)

            
    else :  ##if gender is NOT important, treat all students as 'male' for coding purpose
        males = candidatePool[:]
                
    genders = [males, females, others]

    ##print(males, '\n''\n', females, '\n''\n',others)    ##testcode

    ##Randomize assignments

    if isAbilityImportant:
        for genderGroup in genders:
            i = 0
            while (len(genderGroup) >= 1):
            ##for i in range (len(genderGroup) - 1, -1, -1):
                candidate = genderGroup[i]
                genderGroup.remove(candidate)

                ## If last person
                if len(genderGroup) == 0:
                    notGrouped.append(candidate)
                else:
                    abilityPool = []  ##stores the gendered students within 1 ability point of the candidate
                    for partner in genderGroup:
                        oldestGroupNum = 4
                        newestGroupNum = 5
                        if abs(candidate[3] - partner[3]) <= 1 and \
                        not(candidate[oldestGroupNum] == partner[oldestGroupNum]) or (candidate[newestGroupNum] == partner[newestGroupNum]):
                            abilityPool.append(partner)
                    ## If no one was great match
                    if len(abilityPool) == 0:
                        for partner in genderGroup:
                            newestGroupNum = 5
                            if abs(candidate[3] - partner[3]) <= 1 and \
                            candidate[newestGroupNum] != partner[newestGroupNum]:
                                abilityPool.append(partner)

                    ## this will probably pair them with their most recent partner... OR we could just put them in the not grouped pool (judgement call)
                    if len(abilityPool) == 0:
                        for partner in genderGroup:
                            if abs(candidate[3] - partner[3]) <= 1:
                                abilityPool.append(partner)

                    #no ability match is left
                    if (len(abilityPool) == 0):
                        ##isMatched = True
                        notGrouped.append(candidate)
                    else:
                        rand = random.randint(0, len(abilityPool) -1)
                        partner = abilityPool[rand]
                        newEntry = []
                        newEntry.append(candidate)
                        newEntry.append(partner)
                        newGroups.append(newEntry)
                        genderGroup.remove(partner)  
    else:  
      for genderGroup in genders:
            i = 0
            while (len(genderGroup) >= 1):
            ##for i in range (len(genderGroup) - 1, -1, -1):
                candidate = genderGroup[i]
                genderGroup.remove(candidate)

                ## If last person
                if len(genderGroup) == 0:
                    notGrouped.append(candidate)
                else:
                    abilityPool = []  ##stores the gendered students within 1 ability point of the candidate
                    for partner in genderGroup:
                        oldestGroupNum = 4
                        newestGroupNum = 5
                        if not(candidate[oldestGroupNum] == partner[oldestGroupNum]) or (candidate[newestGroupNum] == partner[newestGroupNum]):
                            abilityPool.append(partner)
                    ## If no one was great match
                    if len(abilityPool) == 0:
                        for partner in genderGroup:
                            newestGroupNum = 5
                            if candidate[newestGroupNum] != partner[newestGroupNum]:
                                abilityPool.append(partner)

                    ## this will probably pair them with their most recent partner... OR we could just put them in the not grouped pool (judgement call)
                    if len(abilityPool) == 0:
                        for partner in genderGroup:
                            abilityPool.append(partner)

                    #no ability match is left
                    if (len(abilityPool) == 0):
                        ##isMatched = True
                        notGrouped.append(candidate)
                    else:
                        rand = random.randint(0, len(abilityPool) -1)
                        partner = abilityPool[rand]
                        newEntry = []
                        newEntry.append(candidate)
                        newEntry.append(partner)
                        newGroups.append(newEntry)
                        genderGroup.remove(partner)  
        
    print(newGroups)
    print(notGrouped)
    # Randomize the rest of the pairings...
    while len(notGrouped) > 1:
      p1 = random.choice(notGrouped)
      notGrouped.remove(p1)
      p2 = random.choice(notGrouped)
      notGrouped.remove(p2)
      newGroups.append([p1, p2])
    print("Pairing the left over students")
    print(newGroups)
    print(notGrouped)
    return newGroups



                    ##isMatched = False
                    ##while(not isMatched):
                        
                        ##oldestGroupNum = 4
                        ##newestGroupNum = 5
                        ##if not(candidate[oldestGroupNum] == partner[oldestGroupNum]) or (candidate[newestGroupNum] == partner[newestGroupNum]):
    ##                        newGroups.append(candidate)
    ##                        newGroups.append(partner)
    ##                        genderGroup.remove(partner)
    ##                        isMatched = True
    ##                    else:
    ##                        abilityPool.remove(partner)

    
    # print('\n\n--------\n\n')

    # for group in newGroups:
    #     print('\n', group)

    # for person in notGrouped:
    #     print('\n', person)
            
            

## ~~~~FUTURE CODE~~~~ pair using preferred partners
    ##check for preferred partner matches
        ##ensure they weren't grouped together recently
            ##group them if not too recent & remove them from candidate pool
            ##place back in candidate pool
    ##prevent never pairs from being paired, return these to the pool FUTURE CODE


##remember to 
##when sending back new group numbers, increment group numbers indefinitely
##return to the database [id, newGroupNum] for each student





##to do
##deal with an odd number of students - perhaps kick out one of the highest skilled students to work alone???
