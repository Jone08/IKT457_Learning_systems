import random
from random import choice

class Memory:
    def __init__(self, forget_value, memorize_value, memory):
        self.memory = memory
        self.forget_value = forget_value
        self.memorize_value = memorize_value

    def get_memory(self):
        return self.memory
    
    def get_literals(self):
        return list(self.memory.keys())
    
    def get_condition(self):
        condition = []
        for literal in self.memory:
            if self.memory[literal] >= 6:
                condition.append(literal)
        return condition
    
    def memorize(self, literal):
        if random.random() <= self.memorize_value and self.memory[literal] < 10:
            self.memory[literal] += 1

    def forget(self, literal):
        if random.random() <= self.forget_value and self.memory[literal] > 1:
            self.memory[literal] -= 1

    def memorize_always(self, literal):
        if self.memory[literal] < 10:
            self.memory[literal] += 1



cancer_patients = [
    {"lt40": False, "ge40": True, "premono": False, 
     "zero_two": False, "three_five": True, "six_eight": False, 
     "deg_malig_1": False, "deg_malig_2": False, "deg_malig_3": True,},

     {"lt40": False, "ge40": True, "premono": False,
      "zero_two": False, "three_five": False, "six_eight": True,
      "deg_malig_1": False, "deg_malig_2": False, "deg_malig_3": True,},

      {"lt40": False, "ge40": False, "premono": True,
      "zero_two": True, "three_five": False, "six_eight": False,
      "deg_malig_1": False, "deg_malig_2": False, "deg_malig_3": True,},
]


cancer_free_patients = [
    {"lt40": True, "ge40": False, "premono": False, 
     "zero_two": True, "three_five": False, "six_eight": False, 
     "deg_malig_1": False, "deg_malig_2": False, "deg_malig_3": True,},

     {"lt40": False, "ge40": True, "premono": False,
      "zero_two": True, "three_five": False, "six_eight": False,
      "deg_malig_1": False, "deg_malig_2": True, "deg_malig_3": False,},

      {"lt40": False, "ge40": False, "premono": True,
      "zero_two": True, "three_five": False, "six_eight": False,
      "deg_malig_1": True, "deg_malig_2": False, "deg_malig_3": False,},
]


# print(cancer_patients)
# print(cancer_free_patients)


def evaluate_condition(observation, condition):
    truth_value_of_condition = True
    for feature in observation:
        if feature in condition and observation[feature] == False:
            truth_value_of_condition = False
            break
        if 'NOT ' + feature in condition and observation[feature] == True:
            truth_value_of_condition = False
            break
    return truth_value_of_condition


# Rules
R1 = ["deg_malig_3", "NOT lt40"]  # -> Recurrence
R2 = ["deg_malig_3", "NOT lt40"]  # -> Recurrence
R3 = ["zero_two"]  # -> Non-recurrence

n = 1
print(f"\n###### Rule 1 ######")
for i in range(len(cancer_patients)):
    print(f"Patient {n}, {evaluate_condition(cancer_patients[i], R1)}")
    n += 1 
    print(f"Patient {n}, {evaluate_condition(cancer_free_patients[i], R1)}")
    n += 1
print(f"____________________________________________")

n = 1
print(f"\n###### Rule 2 ######")
for i in range(len(cancer_patients)):
    print(f"Patient {n}, {evaluate_condition(cancer_patients[i], R2)}")
    n += 1 
    print(f"Patient {n}, {evaluate_condition(cancer_free_patients[i], R2)}")
    n += 1
print(f"____________________________________________")

n = 1
print(f"\n###### Rule 3 ######")
for i in range(len(cancer_patients)):
    print(f"Patient {n}, {evaluate_condition(cancer_patients[i], R3)}")
    n += 1 
    print(f"Patient {n}, {evaluate_condition(cancer_free_patients[i], R3)}")
    n += 1
print(f"____________________________________________\n")



def classify2(observation, R1, R2, R3):
    vote_sum = 0
    if evaluate_condition(observation, R1) == True:
        vote_sum += 1
    if evaluate_condition(observation, R2) == True:
        vote_sum += 1
    if evaluate_condition(observation, R3) == True:
        vote_sum -= 1

    print(vote_sum)
    if vote_sum >= 0:
        return "Cancer"
    else:
        return "Cancer free"





for i in range(len(cancer_patients)):
    print(f"{classify2(cancer_patients[i], R1, R2, R3)}")
    print(f"{classify2(cancer_free_patients[i], R1, R2, R3)}")

print(f"____________________________________________\n")



def type_i_feedback(observation, memory):
    remaining_literals = memory.get_literals()
    if evaluate_condition(observation, memory.get_condition()) == True:
        for feature in observation:
            if observation[feature] == True:
                memory.memorize(feature)
                remaining_literals.remove(feature)
            elif observation[feature] == False:
                memory.memorize("NOT " + feature)
                remaining_literals.remove("NOT " + feature)
    for literal in remaining_literals:
        memory.forget(literal)



mem = {
    "lt40": 5, "ge40": 5, "premono": 5, 
    "zero_two": 5, "three_five": 5, "six_eight": 5, 
    "deg_malig_1": 5, "deg_malig_2": 5, "deg_malig_3": 5,

    "NOT lt40": 5, "NOT ge40": 5, "NOT premono": 5, 
    "NOT zero_two": 5, "NOT three_five": 5, "NOT six_eight": 5, 
    "NOT deg_malig_1": 5, "NOT deg_malig_2": 5, "NOT deg_malig_3": 5,
}



cancer_rule = Memory(0.8, 0.2, mem)

for i in range(100):
    observation_id = random.choice([0,1,2])
    type_i_feedback(cancer_patients[observation_id], cancer_rule)


print(cancer_rule.get_memory())

print(f"____________________________________________\n")


def type_ii_feedback(observation, memory):
    if evaluate_condition(observation, memory.get_condition()) == True:
        for feature in observation:
            if observation[feature] == False:
                memory.memorize_always(feature)
            elif observation[feature] == True:
                memory.memorize_always("NOT " + feature)


print(f"IF {" AND ".join(cancer_rule.get_condition())} THEN Cancer")


for i in range(100):
    observation_id = random.choice([0, 1, 2])
    cancer = random.choice([0, 1])
    if cancer == 1:
        type_i_feedback(cancer_patients[observation_id], cancer_rule)
        type_i_feedback(cancer_free_patients[observation_id], cancer_rule)
    else:
        type_ii_feedback(cancer_patients[observation_id], cancer_rule)
        type_ii_feedback(cancer_free_patients[observation_id], cancer_rule)

print(f"IF {" AND ".join(cancer_rule.get_condition())} THEN Cancer")


print(cancer_rule.get_memory())

print(f"___________________________________________________________________\n")



def classify_patient(observation, pos_rules, neg_rules):
    vote_sum = 0
    for pos_rule in pos_rules:
        if evaluate_condition(observation, pos_rule.get_condition()) == True:
            vote_sum += 1
    for neg_rule in neg_rules:
        if evaluate_condition(observation, neg_rule.get_condition()) == True:
            vote_sum -= 1

    if vote_sum >= 0:
        return "Cancer"
    else:
        return "Cancer free"
    
    

print(f"____________________________________________\n____________________________________________\n")



def train(cancer_patients, cancer_free_patients, cancer_rule, cancer_free_rule, iterations=100):

    for _ in range(iterations):
        observation_id = choice([0, 1, 2])
        cancer = choice([0, 1])
        if cancer == 1:
            type_i_feedback(cancer_patients[observation_id], cancer_rule)
        else:
            type_ii_feedback(cancer_free_patients[observation_id], cancer_rule)


    for _ in range(iterations):
        observation_id = choice([0, 1, 2])
        cancer = choice([0, 1])
        if cancer == 1:
            type_i_feedback(cancer_free_patients[observation_id], cancer_free_rule)
        else:
            type_ii_feedback(cancer_patients[observation_id], cancer_free_rule)




cancer_mem = {
    "lt40": 5, "ge40": 5, "premono": 5, 
    "zero_two": 5, "three_five": 5, "six_eight": 5, 
    "deg_malig_1": 5, "deg_malig_2": 5, "deg_malig_3": 5,

    "NOT lt40": 5, "NOT ge40": 5, "NOT premono": 5, 
    "NOT zero_two": 5, "NOT three_five": 5, "NOT six_eight": 5, 
    "NOT deg_malig_1": 5, "NOT deg_malig_2": 5, "NOT deg_malig_3": 5,
}

cancer_free_mem = {
    "lt40": 5, "ge40": 5, "premono": 5, 
    "zero_two": 5, "three_five": 5, "six_eight": 5, 
    "deg_malig_1": 5, "deg_malig_2": 5, "deg_malig_3": 5,

    "NOT lt40": 5, "NOT ge40": 5, "NOT premono": 5, 
    "NOT zero_two": 5, "NOT three_five": 5, "NOT six_eight": 5, 
    "NOT deg_malig_1": 5, "NOT deg_malig_2": 5, "NOT deg_malig_3": 5,
}


cancer_recurrence = 0
cancer_free_recurrence = 0

cancer_rule = Memory(0.8, 0.2, cancer_mem)
cancer_free_rule = Memory(0.8, 0.2, cancer_free_mem)

for _ in range(400):

    train(cancer_patients, cancer_free_patients, cancer_rule, cancer_free_rule, iterations=100)

    for j in range(3):
        if classify_patient(cancer_patients[j], [cancer_rule], [cancer_free_rule]) == "Cancer":
            cancer_recurrence += 1
    

    for j in range(3):
        if classify_patient(cancer_free_patients[j], [cancer_rule], [cancer_free_rule]) == "Cancer free":
            cancer_free_recurrence += 1


print(f"Recurrence rule: {cancer_rule.get_condition()}")
print(f"Non-recurrence rule: {cancer_free_rule.get_condition()}\n")

print(f"Cancer patients: {cancer_recurrence} / {400 * 3}")
print(f"Cancer free patients: {cancer_free_recurrence} / {400 * 3}")
print(f"Total: {cancer_recurrence + cancer_free_recurrence} / {400 * 6}")



print(f"____________________________________________\n____________________________________________\n")



cancer_mem = {
    "lt40": 5, "ge40": 5, "premono": 5, 
    "zero_two": 5, "three_five": 5, "six_eight": 5, 
    "deg_malig_1": 5, "deg_malig_2": 5, "deg_malig_3": 5,

    "NOT lt40": 5, "NOT ge40": 5, "NOT premono": 5, 
    "NOT zero_two": 5, "NOT three_five": 5, "NOT six_eight": 5, 
    "NOT deg_malig_1": 5, "NOT deg_malig_2": 5, "NOT deg_malig_3": 5,
}

cancer_free_mem = {
    "lt40": 5, "ge40": 5, "premono": 5, 
    "zero_two": 5, "three_five": 5, "six_eight": 5, 
    "deg_malig_1": 5, "deg_malig_2": 5, "deg_malig_3": 5,

    "NOT lt40": 5, "NOT ge40": 5, "NOT premono": 5, 
    "NOT zero_two": 5, "NOT three_five": 5, "NOT six_eight": 5, 
    "NOT deg_malig_1": 5, "NOT deg_malig_2": 5, "NOT deg_malig_3": 5,
}


cancer_recurrence = 0
cancer_free_recurrence = 0

cancer_rule = Memory(0.5, 0.5, cancer_mem)
cancer_free_rule = Memory(0.5, 0.5, cancer_free_mem)

for _ in range(400):

    train(cancer_patients, cancer_free_patients, cancer_rule, cancer_free_rule, iterations=100)

    for j in range(3):
        if classify_patient(cancer_patients[j], [cancer_rule], [cancer_free_rule]) == "Cancer":
            cancer_recurrence += 1
    

    for j in range(3):
        if classify_patient(cancer_free_patients[j], [cancer_rule], [cancer_free_rule]) == "Cancer free":
            cancer_free_recurrence += 1


print(f"Recurrence rule: {cancer_rule.get_condition()}")
print(f"Non-recurrence rule: {cancer_free_rule.get_condition()}\n")

print(f"Cancer patients: {cancer_recurrence} / {400 * 3}")
print(f"Cancer free patients: {cancer_free_recurrence} / {400 * 3}")
print(f"Total: {cancer_recurrence + cancer_free_recurrence} / {400 * 6}")





print(f"____________________________________________\n____________________________________________\n")



cancer_mem = {
    "lt40": 5, "ge40": 5, "premono": 5, 
    "zero_two": 5, "three_five": 5, "six_eight": 5, 
    "deg_malig_1": 5, "deg_malig_2": 5, "deg_malig_3": 5,

    "NOT lt40": 5, "NOT ge40": 5, "NOT premono": 5, 
    "NOT zero_two": 5, "NOT three_five": 5, "NOT six_eight": 5, 
    "NOT deg_malig_1": 5, "NOT deg_malig_2": 5, "NOT deg_malig_3": 5,
}

cancer_free_mem = {
    "lt40": 5, "ge40": 5, "premono": 5, 
    "zero_two": 5, "three_five": 5, "six_eight": 5, 
    "deg_malig_1": 5, "deg_malig_2": 5, "deg_malig_3": 5,

    "NOT lt40": 5, "NOT ge40": 5, "NOT premono": 5, 
    "NOT zero_two": 5, "NOT three_five": 5, "NOT six_eight": 5, 
    "NOT deg_malig_1": 5, "NOT deg_malig_2": 5, "NOT deg_malig_3": 5,
}


cancer_recurrence = 0
cancer_free_recurrence = 0

cancer_rule = Memory(0.2, 0.8, cancer_mem)
cancer_free_rule = Memory(0.2, 0.8, cancer_free_mem)

for _ in range(400):

    train(cancer_patients, cancer_free_patients, cancer_rule, cancer_free_rule, iterations=100)

    for j in range(3):
        if classify_patient(cancer_patients[j], [cancer_rule], [cancer_free_rule]) == "Cancer":
            cancer_recurrence += 1
    

    for j in range(3):
        if classify_patient(cancer_free_patients[j], [cancer_rule], [cancer_free_rule]) == "Cancer free":
            cancer_free_recurrence += 1


print(f"Recurrence rule: {cancer_rule.get_condition()}")
print(f"Non-recurrence rule: {cancer_free_rule.get_condition()}\n")

print(f"Cancer patients: {cancer_recurrence} / {400 * 3}")
print(f"Cancer free patients: {cancer_free_recurrence} / {400 * 3}")
print(f"Total: {cancer_recurrence + cancer_free_recurrence} / {400 * 6}")


