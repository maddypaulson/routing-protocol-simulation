# Data to write
data_to_write = "This is the data from distance-vector."

# Open file and create if it doesn't exist
with open('output.txt', 'w') as file:
    file.write(data_to_write)
