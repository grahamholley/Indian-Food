##########################################################################
# Computer Project #9
#   Algorithm
#       Open file of indian food data for reading.
#       Build a dictionary of the data using the file pointer.
#       Display Menu and prompt user for an input, re-prompting for invalid inputs.
#           Options are A,B,C,D,Q. Q quits the program 
#       If user inputs 'A' prompt for foods and display ingredients of those foods.
#       If user inputs 'B' prompt for ingredients and display foods that have them. 
#       If user inputs 'C' prompt for foods and ingredients and display useful and missing ingredients
#       If user inputs 'D' prompt for preferences and display food with those preferences.
#       Thank the user for playing.
##########################################################################

#from the project desription: "This project focuses on analyzing a publicly available
# dataset (https://www.kaggle.com/nehaprabhavalkar/indian-food-101)(slightly modified to remove edge cases)
# containing several hundred Indian food, their region and
# state of origin, and their necessary ingredients etc."


import csv
from operator import itemgetter

def open_file(s):
     """
    Parameters
    ----------
    s : int
        int identifier for file pointer.

    Returns
    -------
    file_pointer : variable assigned file pointer
Function takes in int and uses it to open file as file pointer

    """
     while True:
        #runs until return
        try:
            file_name = input('Input a {} file: '.format(s))
            #prompt user for input of file name
            file_pointer = open(file_name, 'r')
            #open a read file assigned to file_pointer
            return file_pointer
            #return file_pointer
        except FileNotFoundError:
            #if try code suite cannot be run then except suite runs
            print('Invalid filename, please try again.')
            #print error message if file cannot be opened
            
def build_dictionary(fp):
    """

    Parameters
    ----------
    fp : file pointer assignment
        file pointer of indian food file data.

    Returns
    -------
    superD : dictionary
        dictionary of nested dictionaries of indian food data.
Function reads indian food data from the file and makes it into a dictionary
    """
    reader = csv.reader(fp)
    header = next(reader,None)
    #assign reader for csv file and skip header
    superD = {}
    for line in reader:
        region = line[8].strip()
        state = line[7].strip()
        flavor = line[5].strip()
        cook_time = int(line[4].strip())
        prep_time = int(line[3].strip())
        diet = line[2].strip()
        food = line[0].strip()
        #assign different data points of the file to variabes.
        ingredients_list = line[1].lower().strip().split(',')
        #make list of ingredients removing whitespace
    
        sets = set()
        for i in ingredients_list:
            sets.add(i.strip())
            #make ingredients list into a set
        tuples = tuple((prep_time, cook_time))
        #create tuple of cook times
        lists = []
        lists.append(sets)
        lists.append(diet)
        lists.append(tuples)
        lists.append(flavor)
        #append food values to list
        if '-1' in line:
            continue
        #skip rows with missing values
        elif region not in superD:
            superD[region] = {}
            if state not in superD[region]:
                superD[region][state] = {}
                #if region and then state do not yet ecist in the exist, create 
                #keys for them with dictionaries as values
        else:
            if state not in superD[region]:
                superD[region][state] = {}
            #account for cases where region is already in the dictionary but state is not
        if region in superD:
            if state in superD[region]:
                superD[region][state][food] = lists
                #add key:value pairs of list as value and food as key in the 
                #corresponding state dictionary values
            
    return superD
            
        
    

def get_ingredients(D,L):
    """

    Parameters
    ----------
    D : dict
        indian food data dictionary.
    L : lst
        list of desired foods.
Function takes in indian food dictionary data and desired foods and ouputs
 ingredients of desired foods.
    Returns
    -------
    sets : TYPE
        DESCRIPTION.

    """
    sets = set()
    for i in L: 
        for region in D:
            for state in D[region]:
                for key,value in D[region][state].items():
                    #loop through region, state and food keys
                    if key.strip() == i.strip():
                        
                        for n in value[0]:
                            sets.add(n)
    #if food in parameter list matches food in loop, loop through its ingreients
    #and append them to the set
                            
    
    return sets

                        

def get_useful_and_missing_ingredients(D, foods, pantry):
    """

    Parameters
    ----------
    D : dict
        dictionary of indian food data.
    foods : lst
        list of desired foods.
    pantry : lst
        list of ingredients already available.

    Returns
    -------
    useful : lst
        list of useful ingredients.
    missing : lst
        list of missing ingredients
Function takes in desired foods and ingredients that the user already has and 
outputs useful ingredients and missing ingredients
    """
    sets = get_ingredients(D, foods)
    sets_list = list(sets)
    #make set of required ingredients into a list
    useful = []
    missing = []
    for i in pantry:
        if i in sets_list:
            useful.append(i)
            #append needed ingredients already obtained to useful list
    for i in sets_list:
        if i.strip() not in pantry:
            missing.append(i)
        #append needed ingredients not already obtained to missing list
    
    return sorted(useful), sorted(missing)

def get_list_of_foods(D, L):
    """

    Parameters
    ----------
    D : dict
        dictionary of indian food data.
    L : lst
        ingredients list.

    Returns
    -------
    listy : lst
        list of foods.
Function takes in list of ingredients and returns all foods that can be made with them
    """
    foods = []
    listy = []
    sets = set()
    for i in L:
        sets.add(i.strip())
        #make ingredients from list input into a set
    for region in D:
            for state in D[region]:
                for key,value in D[region][state].items():
                    
                    if sets.issuperset(value[0]) == True:
                        time = sum(value[2])
                        #calculate cook time for sorting
                        pair = tuple((key, time))
                        #makes tuples of food name and cook time
                        
                        foods.append(pair)
                    #loop through food key:value pairs in region, state dicts and append
                    #foods that share the ingredients of the input to the list of foods
    
    for i in sorted(foods, key = itemgetter(1,0)):
        #sort by cook time and then by alphabet
        listy.append(i[0])
        #only take sorted food names into new list for return
    return listy
    
def get_food_by_preference(D, preferences):
    """
    Parameters
    ----------
    D : dict
        dictionary of indian food data.
    preferences : lst
        list of food preferences.
    Returns
    -------
    lst
        list of foods that match preferences.
Function takes in preferences and returns food with those preferences
    """
    lists = []
    for region in D:
        if region.strip() in preferences or preferences[0] == None:
            for state in D[region]:
                if state in preferences or preferences[1] == None:
            #if values in preferences are None, use all values of that preference
                    for key, value in D[region][state].items():
                        if value[1] in preferences and value[3] in preferences:
                            lists.append(key)
                #if region, state, diet, and taste preferences match input, append food to list
    return sorted(lists)

def main():  
    
    choices = ['A', 'B', 'C', 'D', 'Q']
    print("Indian Foods & Ingredients.\n")    
    fp = open_file('indian_food')
    D = build_dictionary(fp)          
    #open file for reading and use file pointer to create a dictionary of the data
    MENU = '''
        A. Input various foods and get the ingredients needed to make them!
        B. Input various ingredients and get all the foods you can make with them!
        C. Input various foods and ingredients and get the useful and missing ingredients!
        D. Input various foods and preferences and get only the foods specified by your preference!
        Q. Quit
        : '''
    
    prompt = input(MENU)
    prompt = prompt.upper()
    #prompt user for menu choices and account for capitalization
    while prompt not in choices:
        print("Invalid input. Please enter a valid input (A-D, Q)")
        prompt = input(MENU)
        prompt = prompt.upper()
        #error check for invalid inputs
    while not prompt == 'Q':
        #'Q' to quit
        if prompt == 'A':
            foody = input('Enter foods, separated by commas: ').split(',')
            #prompt for foods input and make it a list
            sets = get_ingredients(D, foody)
            #get ingredients for foods
            foods = ''
            lst = list(sorted(sets))
            #make ingredient set into a sorted list
            print('Ingredients: ')
            for i in sorted(sets):
                if i == lst[-1]:
                    cons = i
                else:
                    cons = i + ', '
                foods += cons
            print(foods)
            #print ingredients with commas except for last
        elif prompt == 'B':
            ingredients = input('Enter ingredients, separated by commas: ').split(',')
            #make ingredients input into a list
            listy = get_list_of_foods(D, ingredients)
            print('Foods: ')
            #get list of foods with input ingredients
            ingry = ''
            for i in listy:
                if i == listy[-1]:
                    ing = i
                else:
                    ing = i + ', '
                ingry += ing
            print(ingry)
            #print foods with input ingredients with commas except for last
        elif prompt == 'C':
            foods = input('Enter foods, separated by commas: ').strip().split(',')
            #make list of input foods
            for i,ch in enumerate(foods):
                foods[i] = foods[i].strip()
                #remove white space from list values
            pantry = input('Enter ingredients, separated by commas: ').strip().split(',')
            #makes list of input pantry ingredients
            for i,ch in enumerate(pantry):
                pantry[i] = pantry[i].strip()
                #remove white space from list values
            useful, missing = get_useful_and_missing_ingredients(D, foods, pantry)
            #get useful and missing ingredients
            print ('Useful Ingredients: ')
            use = ''
            for i in useful:
                if i == useful[-1]:
                    cons = i
                else:
                    cons = i + ', '
                use += cons
            print(use)
            mis = ''
            print('Missing Ingredients: ')
            for i in missing:
                if i == missing[-1]:
                    var = i
                else:
                    var = i + ', '
                mis += var
            print(mis)
            #print useful and missing ingredients with commas except for last
        elif prompt == 'D':
            preferences = input('Enter preferences, separated by commas: ').strip().split(',')
            #amke list of input preferences
            for i,ch in enumerate(preferences):
                preferences[i] = preferences[i].strip()
                #remove white space from list values
            print('Preferred Food: ')
            listerine = get_food_by_preference(D, preferences)
            #get foods with shared preferences
            pref = ''
            for i in listerine:
                if i == listerine[-1]:
                    ind = i
                else:
                    ind = i + ', '
                pref += ind
            print(pref)
            #print foods with preferences with comams except for last
        
        prompt = input(MENU)
        prompt = prompt.upper()
        while prompt not in choices:
            print("Invalid input. Please enter a valid input (A-D, Q)")
            
            #reprompt and display menu after choice
            prompt = input(MENU)
            prompt = prompt.upper()
    print("Thanks for playing!")        

if __name__ == '__main__':
    main()
