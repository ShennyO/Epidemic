import random
from person import Person
from virus import Virus

#In here we're gonna need a lot of shit. Let's think about what we need for the simulation first. A population size,
#How many people are initially infected, what's the virus, the qualities of the virus, how many people are initially vaccinated


#So far we have an exposure function, and we also have a die function. The exposure and the die should run in a loop
#until there is no more alive people who are non_vaccinated

class Simulation(object):
    """docstring for Simulation."""
    def __init__(self, population_size, initially_infected, virus_name, virus_mortality_rate, virus_spread_rate, initial_vaccinated_percentage):

        self.population_size = population_size
        self.initially_infected = initially_infected
        self.virus_name = virus_name
        self.virus_mortality_rate = virus_mortality_rate
        self.virus_spread_rate = virus_spread_rate
        self.initial_vaccinated_percentage = initial_vaccinated_percentage
        self.population = []
    #Ok now let's think about an inside component of our simulation, we need the actual population of people to run the simulation on.



    def add_virus(self):
        virus = Virus(self.virus_name, self.virus_mortality_rate, self.virus_spread_rate)
        return virus


    #we need something to fill up our population

    def create_population(self):

        person_id = 0
    #in this function, we have to create each person, firstly, we have to build the infected people
    #Then, depending on randomness, the other people will be born vaccinated or not
        infected_count = 0
        vaccinated_count = 0

        for x in range(self.population_size):

            if infected_count != self.initially_infected:
                person = Person(person_id, False, self.add_virus(), True)
                person_id +=1
                infected_count +=1
                self.population.append(person)

            else:

                #Now that we have the infected people done, we can tackle the rest of the people, whether they are vaccinated or not
                #we need to test a random number against the vaccinated percentage, we need a float between 0, 1
                luck_of_the_draw = random.random()
                if luck_of_the_draw < self.initial_vaccinated_percentage:
                    #if the luck is less than the vaccinated percentage, that person will be vaccinated
                    person = Person(person_id, True, None, True)
                    person_id+=1
                    vaccinated_count +=1
                    self.population.append(person)

                else:
                    person = Person(person_id, False, None, True)
                    person_id+=1
                    self.population.append(person)



        print("infected_count: %s " % infected_count)
        print("vaccinated_count: %s" % vaccinated_count)
        print("population size: %s" % len(self.population))
        return self.population

    #This function randomly picks 100 random people from all the alive people
    # def pick_100(self, alive_group, random_added_ppl):
    #     while random_added_ppl != 100:
    #         random_num = random.randint(0, len(alive_group)-1)
    #
    #         if random_num not in used_numbers:
    #             random_group.append(alive_group[random_num])
    #             used_numbers.append(random_num)
    #         else:
    #         #go back to the top of this while loop
    #         pick_100()


    #We need an exposure method where the infected is interacting with a set amount of people
    def exposure(self):
        #everytime we run this function we need to pick 100 random alive people to test against, if at least one of those
        #people are infected, everyone in that 100 group who are non_vaccinated will be exposed to the virus
        alive_group = []

        #getting a list of all the people who are alive
        for person in self.population:
            if person.is_alive:
                alive_group.append(person)

        random_group = []
        random_added_ppl = 0
        infected_present = False
        used_numbers = []
        randoms_infected_count = 0

        #here, we're saying do this 100 times
        while random_added_ppl != 100:
            #each time we get a random number between 0 and the number of alive ppl - 1, representing one person
            random_num = random.randint(0, len(alive_group)-1)


            #after we get the random number, we can't use that specific random number anymore.
            #adding a random person to the random group of ppl, there should be 100 people in here.
            #I should change it to a while loop and do it by count of added people
            #if the random number has never been used before, we can add that random person into our array,
            #But if its been used before, I want to restart the while loop from the top, gotta research how to do that.
            if random_num not in used_numbers:
                random_group.append(alive_group[random_num])
                used_numbers.append(random_num)
                random_added_ppl +=1
            else:
                continue
                #go back to the top of this while loop

        #Here we are looping through the 100 random people we pulled. If there is just 1 infected person present, we'll
        #expose those 100 people to the infection
        for person in random_group:
            if person.infection != None:
                infected_present = True

        if infected_present:
            for person in random_group:
                immune_strength = random.random()
                if immune_strength<self.virus_spread_rate:
                    person.infection = self.add_virus()
                    randoms_infected_count +=1

        print("%s got infected" % randoms_infected_count)




    #In this function we are going to test the people who are infected, see if they die or not
    def die(self):
        non_vaccinated = []
        dead = 0
        alive = 0

        #moving all the non_vaccinated people into a group
        for person in self.population:
            if person.is_vaccinated == False:
                non_vaccinated.append(person)
        print("non_vaccinated: %s" % len(non_vaccinated))

        for person in non_vaccinated:
            person.unleashed_infection()

        for person in non_vaccinated:
            if person.is_alive == True:
                alive +=1
            elif person.is_alive == False:
                dead+=1

        print("dead: %s" % dead)

        print("alive: %s" % alive)






sim = Simulation(100, 10, "Malaria", .03, .01, .25)
sim.create_population()
sim.exposure()
sim.die()
