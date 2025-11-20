#Sentinel Loops (cause loops to end)
# this loop ends when a user puts the sentinel value
sentinel = 999
input_value = 0

while input_value != sentinel:
    input_value = int(input("Enter your number or type 999 to stop: "))