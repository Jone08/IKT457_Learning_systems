import random

class Environment:
    def penalty(self, m):
        if m <= 3:
            if random.random() < m * 0.2:
                return False
            else:
                return True
        else:
            if random.random() < 0.6 - (m - 3) * 0.2:
                return False
            else:
                return True

class Tsetlin:
    def __init__(self, n):
        self.n = n
        self.state = random.choice([self.n, self.n + 1]) 

    def reward(self):
        if 1 < self.state <= self.n:
            self.state -= 1
        elif self.n < self.state < 2 * self.n:
            self.state += 1

    def penalize(self):
        if self.state <= self.n:
            self.state += 1
        else:
            self.state -= 1

    def makeDecision(self):
        if self.state <= self.n:
            return 1 # Yes
        else: 
            return 0 # No
        

def main():

    env = Environment()

    iterations = 200
    machine_count = [0] * 5
    machines = []

    for i in range(5):
        machines.append(Tsetlin(20))


    for i in range(iterations):
        
        m = 0
        count = 0

        for j in machines:
            action = j.makeDecision()
            if action == 1:
                m += 1
                machine_count[count] += 1
            count += 1
        

        for j in machines:
            penalty2 = env.penalty(m)
            if penalty2:
                j.penalize()
            else:
                j.reward()

    
    for i in range(len(machine_count)):
        print(f"Machine {i + 1}: {machine_count[i]}")


if __name__ == "__main__":
    main()

