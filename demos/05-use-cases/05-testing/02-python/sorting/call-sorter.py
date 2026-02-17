from sorting import ObjectSorter

# Create a list of dictionaries
objects = [{'name': 'John', 'age': 30}, {'name': 'Jane', 'age': 25}, {'name': 'Doe', 'age': 35}]

# Create an instance of ObjectSorter
sorter = ObjectSorter(objects)

# Sort the objects by age in ascending order
sorted_objects = sorter.sort('age', ascending=True)

# Print the sorted objects
print(sorted_objects)