def calculate_averages(data):
    # Initialize a dictionary to hold the sums of each item
    sums = {}
    # Initialize a dictionary to hold the counts of each item
    counts = {}

    # Iterate through each dictionary in the list
    for entry in data:
        for key, value in entry.items():
            # Add value to the sum for this key
            if key in sums:
                sums[key] += value
                counts[key] += 1
            else:
                sums[key] = value
                counts[key] = 1

    # Calculate the averages
    averages = {key: sums[key] / counts[key] for key in sums}

            # Find the item with the highest average score
    max_item = max(averages, key=averages.get)
    max_average = averages[max_item]

    return averages, max_item