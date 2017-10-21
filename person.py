import random

#In this file we make a Person Class
#in each person, we have to keep track if they are alive, if they are infected, if they survived the infection and are now vaccinated,
#And we also have to keep track of each individual person.
class  Person(object):
    """docstring for  Person."""
    def __init__(self, _id, is_vaccinated, infection, is_alive):
        self._id = _id
        self.is_vaccinated = is_vaccinated
        self.infection = infection
        self.is_alive = is_alive

    #We need a way for each person to interact with the virus, so since every single person has to go through this
    #we'll make a function inside the person class

    #this function will only be run on the people who have not been vaccinated and who are not dead
    def unleashed_infection(self):
        #if the person is infected, we run a random test. If the person's ran_num is greater than the mortality rate,
        #they will survive the infection, become vaccinated and won't carry the infection anymore
        if self.infection != None:
            ran_num = random.random()

            if ran_num < self.infection.mortality_rate:
                self.is_alive = False
                self.infection = None
            else:
                self.is_vaccinated = True
                self.infection = None
