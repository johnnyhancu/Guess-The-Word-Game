import statistics
import matplotlib.pyplot as plt

file = open("Winners_Simulation_Mode.csv")
dataIn=file.read()
file.close
Winners=dataIn.split(",")
Winners_Id=[int(item) for item in Winners]

Winning_players=['Player1', 'Player2', 'Player3']

Frequency=[]

for n in range(3):
    Frequency.append(Winners_Id.count(n+1))

print(Frequency)

plt.bar(Winning_players, Frequency)
plt.xlabel("Winning Player")
plt.title("WINNING PLAYER FREQUENCY IN SIMULATION MODE")
plt.ylabel("Frequency")
plt.show()