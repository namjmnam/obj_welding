import os
from tkinter import filedialog
from package.utils import get_faces
from package.utils import nan_correct
import time

# Start the timer
start_time = time.time()

# Get the script directory
script_directory = os.path.dirname(os.path.abspath(__file__))

obj_file = filedialog.askopenfilename(filetypes=[("OBJ files", "*.obj")], initialdir=script_directory+'/obj')
print(obj_file)

# Initialize an empty list to hold the line numbers
nan_vertices = []

print("Fetching all lines with nan...")
# Get all lines with "nan"
with open(obj_file, 'r') as file:
    # Enumerate over each line in the file, starting with line number 1
    for line_number, line in enumerate(file, 1):
        # Check if "nan" is in the line
        if "nan" in line:
            # Add the line number to the list
            nan_vertices.append(line_number)

# End the timer
end_time = time.time()
time_taken = end_time - start_time
print(f"Time taken to fetch: {time_taken} seconds")
# Start the timer
start_time = time.time()

# print("All nans")
# print(nan_vertices)

print("Fetching list of faces...")
# Get all lists of faces
faces = get_faces(obj_file)
# print(faces)

# End the timer
end_time = time.time()
time_taken = end_time - start_time
print(f"Time taken to fetch: {time_taken} seconds")
# Start the timer
start_time = time.time()

print("Creating a list of faces without nan...")
# print("Faces without nans")
filtered_faces = [f for f in faces if not any(v in nan_vertices for v in f)]
# print(filtered_faces)

# End the timer
end_time = time.time()
time_taken = end_time - start_time
print(f"Time taken to create: {time_taken} seconds")
# Start the timer
start_time = time.time()

print("Creating a list of faces on the edge...")
# print("Faces with nans but not all are nans")
edge_faces = [f for f in faces if any(v in nan_vertices for v in f) and not all(v in nan_vertices for v in f)]
# print(edge_faces)

# End the timer
end_time = time.time()
time_taken = end_time - start_time
print(f"Time taken to create: {time_taken} seconds")
# Start the timer
start_time = time.time()

print("Removing all nan from the edges...")
# print("From edge faces, all nan vertices removed")
cleaned_faces = []
for f in edge_faces:
    # Remove values that are in the first list
    cleaned_list = [value for value in f if value not in nan_vertices]
    cleaned_faces.append(cleaned_list)
# print(cleaned_faces)

# End the timer
end_time = time.time()
time_taken = end_time - start_time
print(f"Time taken to remove: {time_taken} seconds")
# Start the timer
start_time = time.time()

print("Correcting indices of faces with nan eliminated...")
# print("Subtracted and corrected faces with nans eliminated")
modified_faces = nan_correct(filtered_faces, nan_vertices)
# print(modified_faces)

# End the timer
end_time = time.time()
time_taken = end_time - start_time
print(f"Time taken to correct: {time_taken} seconds")
# Start the timer
start_time = time.time()

print("Correcting indices of faces on the edge with nan eliminated...")
# print("Subtracted and corrected cleaned faces with nans eliminated")
modified_cleaned_faces = nan_correct(cleaned_faces, nan_vertices)
# print(modified_cleaned_faces)

# End the timer
end_time = time.time()
time_taken = end_time - start_time
print(f"Time taken to correct: {time_taken} seconds")
# Start the timer
start_time = time.time()

print("Unpacking list of vertices on the edge...")
# print("Vertices located on the edge")
edge_vertices = sorted(set(sum(modified_cleaned_faces, [])))
# print(edge_vertices)

# End the timer
end_time = time.time()
time_taken = end_time - start_time
print(f"Time taken to unpack: {time_taken} seconds")

# Write to the output file
obj_output = filedialog.asksaveasfilename(defaultextension='.obj',
                                        filetypes=[('OBJ files', '*.obj')],
                                        title='Save output file as',
                                        initialfile=f'output.obj',
                                        initialdir=script_directory+'/obj')

# Start the timer
start_time = time.time()

print("Rewriting the output file...")
# Delete all lines that contain "nan"
with open(obj_file, 'r') as input_file, open(obj_output, 'w') as output_file:
    # Iterate over each line in the original file
    for line in input_file:
        # If "nan" is not found in the line, write it to the new file
        if "nan" not in line and "f" not in line:
            output_file.write(line)

    # Add new face lines
    for f in modified_faces:
        # print('f '+' '.join(str(num) for num in f)) 
        output_file.write('f '+' '.join(str(num) for num in f)+'\n')

    # Add triangles from cleaned faces
    for f in modified_cleaned_faces:
        if len(f)>=3:
            output_file.write('f '+' '.join(str(num) for num in f)+'\n')

# End the timer
end_time = time.time()
time_taken = end_time - start_time
print(f"Time taken to rewrite: {time_taken} seconds")
