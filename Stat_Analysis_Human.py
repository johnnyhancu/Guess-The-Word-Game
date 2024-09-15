import statistics
import matplotlib.pyplot as plt
file = open("Stats_Human_Players.csv")
dataIn=file.read()
file.close
NumberOfWrongGuesses=dataIn.split(",")
NumberOfWrongGuessesList=[int(item) for item in NumberOfWrongGuesses]

mean=statistics.mean(NumberOfWrongGuessesList)
mean=round(mean,1)
median=statistics.median(NumberOfWrongGuessesList)
print(f"MEAN VALUE IS {mean}")
print(f"MEDIAN VALUE IS {median}")
#next piece of code calculates the frequency of the number of wrong guesses 
Wrong_Guesses=[]
Frequency=[]
for number in NumberOfWrongGuessesList:
    if number not in Wrong_Guesses:
        Wrong_Guesses.append(number)
Wrong_Guesses.sort()
for item in Wrong_Guesses:
    Frequency.append(NumberOfWrongGuessesList.count(item))


plt.bar(Wrong_Guesses, Frequency)
plt.xlabel("Number of Wrong Guesses")
plt.title("HUMAN PLAYERS WRONG GUESSES FREQUENCIES")
plt.ylabel("Frequency")
plt.show()