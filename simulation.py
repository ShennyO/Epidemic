import random
from person import Person
from virus import Virus
import pdb
from logger import Logger



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
        self.infected = 10
        self.file_name = "epidemic.txt"

        self.logger = Logger(self.file_name)

        # pop_size, vacc_percentage, virus_name, mortality_rate,
                          # basic_repro_num
        self.logger.write_metadata(self.population_size, self.initial_vaccinated_percentage, self.virus_name, self.virus_mortality_rate, self.virus_spread_rate)


    def add_virus(self):
        virus = Virus(self.virus_name, self.virus_mortality_rate, self.virus_spread_rate, 0)
        return virus



    def create_population(self):

        person_id = 0
        infected_count = 0
        vaccinated_count = 0
        not_vacc = 0

        for x in range(self.population_size):

            if infected_count != self.initially_infected:
                person = Person(person_id, False, self.add_virus(), True)
                person_id +=1
                infected_count +=1
                self.population.append(person)

            else:

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
                    not_vacc+=1
                    self.population.append(person)



        print("Created Population")
        print("infected_count: %s " % infected_count)
        print("not vaccinated :( : %s " % not_vacc)
        print("vaccinated_count: %s" % vaccinated_count)
        print("population size: %s" % len(self.population))
        return self.population



    def exposure(self):


        for people in self.population:
            if people.infection != None:
                people.infection.level =1

        alive_group = []

        for person in self.population:
            if person.is_alive:
                alive_group.append(person)


        random_group = []
        random_added_ppl = 0
        infected_present = False
        used_numbers = []
        randoms_infected_count = 0
        infected_ppl = []

        non_vac = 0

        _dead = 0
        _vaccinated = 0
        _infected = 0


        for person in self.population:
            if person.infection != None:
                infected_ppl.append(person)

        for index, infected_person in enumerate(infected_ppl):
            while random_added_ppl != 10:
                random_num = random.randint(0, len(alive_group)-1)

                if random_num not in used_numbers:
                    random_group.append(alive_group[random_num])
                    used_numbers.append(random_num)
                    random_added_ppl +=1
                else:
                    continue
            # print(random_added_ppl)

            for person in random_group:
                if person.infection != None:
                    infected_present = True


            if infected_present:
                for person in random_group:
                    if person.is_vaccinated == False:
                        immune_strength = random.random()
                        if immune_strength<self.virus_spread_rate:
                            person_id = person._id
                            #The logger function should be called right below the add_virus
                            if person.infection == None:
                                self.population[person_id].infection = self.add_virus()
                                self.logger.log_infected(infected_person, person)
                                randoms_infected_count +=1
                            else:
                                self.logger.log_already_infected(infected_person, person)
                        else:
                            self.logger.log_not_infected(person, infected_person)
                    else:
                        self.logger.log_vaccinated(infected_person, person)






        for person in self.population:
            if person.is_vaccinated == False and person.is_alive == True and person.infection == None:
                non_vac+=1
        for person in self.population:
            if person.is_vaccinated == True:
                _vaccinated+=1
        for person in self.population:
            if person.is_alive == False:
                _dead+=1
        for person in self.population:
            if person.infection != None:
                _infected+=1


        print("exposed")
        print("%s are not vaccinated" % non_vac)
        print("%s are vaccinated" % _vaccinated)
        print("%s are dead" % _dead)
        print("%s are infected" % _infected)
        print("\n")



        # print("Round %s:" % _round)





    #In this function we are going to test the people who are infected, see if they die or not
    def die(self):
        infected = []
        dead = 0
        alive = 0
        non_vac = 0
        _round = 1
        _dead = 0
        _vaccinated = 0
        _infected = 0

        #moving all the infected people into a group
        for person in self.population:
            if person.is_vaccinated == False and person.infection != None and person.infection.level ==1:
                infected.append(person)
        # print("non_vaccinated: %s" % len(non_vaccinated))

        for person in infected:

            selected_person_id = person._id
            self.population[selected_person_id].unleashed_infection()

        # for person in infected:
        #     if person.is_alive:
        #         alive +=1
        #     else:
        #         dead+=1

        for person in self.population:
            if person.is_vaccinated == False and person.is_alive == True and person.infection == None:
                non_vac+=1
        for person in self.population:
            if person.is_vaccinated == True:
                _vaccinated+=1
        for person in self.population:
            if person.is_alive == False:
                _dead+=1
        for person in self.population:
            if person.infection != None:
                _infected+=1


        # print("Round %s:" % _round)
        print("death")
        print("%s are not vaccinated" % non_vac)
        print("%s are vaccinated" % _vaccinated)
        print("%s are dead" % _dead)
        print("%s are infected" % _infected)
        print("\n")
        # print("dead: %s" % dead)
        #
        # print("alive: %s" % alive)

    #Now we have a lot of our components done. We have our population creaated, we have our exposure function
    #and we have a mortality function. We need to loop through the exposure and death functions until we have
    #no more unvaccinated alive people.

    def main(self):

        self.create_population()
        non_vac = 0
        _round = 1
        _dead = 0
        _vaccinated = 0
        _infected = 0


        #Get an initial count of how many people are infected
        for people in self.population:
            if people.infection != None:
                _infected +=1



        while _infected != 0:
            print("Round %s:" % _round)
            self.exposure()
            self.die()
            #After we run our simulation for the 100 people, reset the numbers and recount through our people

            _infected = 0

            #get a count of how many alive/non_vaccinated ppl there are


            for person in self.population:
                if person.infection != None:
                    _infected+=1





            _round+=1


            #after each instance of exposure and die, we have to track some details.
            #Finish the rest tomorrow













sim = Simulation(500, 50, "Malaria", .30, .15, .25)
sim.main()

# sim.create_population()
# sim.exposure()
# sim.die()
# sim.exposure()
# sim.die()
# sim.exposure()
# sim.die()
# sim.exposure()
# sim.die()
# sim.exposure()
# sim.die()
# sim.exposure()
# sim.die()
