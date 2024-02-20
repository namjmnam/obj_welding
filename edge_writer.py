import os
from tkinter import filedialog
from package.utils import get_faces
from package.utils import nan_correct
from package.utils import count_vertices
import time

# Get the script directory
script_directory = os.path.dirname(os.path.abspath(__file__))

# Needed for triangles
xMax = 500

obj_file = filedialog.askopenfilename(filetypes=[("Original floor or celing OBJ file", "*.obj")], initialdir=script_directory+'/obj')
print("Original:", obj_file)

# Start the timer
start_time = time.time()

# Initialize an empty list to hold the line numbers
print("Fetching nan indices...")
nan_vertices = []

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
print(f"Time taken for fetching: {time_taken} seconds")
# Start the timer
start_time = time.time()

print("Fetching all faces...")
# Get all lists of faces
faces = get_faces(obj_file)
# print(faces)

# End the timer
end_time = time.time()
time_taken = end_time - start_time
print(f"Time taken for fetching: {time_taken} seconds")
# Start the timer
start_time = time.time()

print("Creating edge faces...")
# print("Faces with nans but not all are nans")
edge_faces = [f for f in faces if any(v in nan_vertices for v in f) and not all(v in nan_vertices for v in f)]
# print(edge_faces)

# End the timer
end_time = time.time()
time_taken = end_time - start_time
print(f"Time taken for creating: {time_taken} seconds")
# Start the timer
start_time = time.time()

print("Removing all nan vertices...")
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
print(f"Time taken for removing: {time_taken} seconds")
# Start the timer
start_time = time.time()

print("Applying triangles algorithm...")
# Now, triangles algorithm
for f in cleaned_faces:
    if len(f)==3:
        # 좌상/우상
        if f[1]-f[0]==1:
            # 좌상
            if f[2]-f[0]==xMax:
                f.pop(0)
            # 우상
            elif f[2]-f[0]==xMax+1:
                f.pop(1)

        # 좌하/우하
        elif f[1]-f[2]==1:
            # 좌하
            if f[1]-f[0]==xMax+1:
                f.pop(2)
            # 우하
            elif f[1]-f[0]==xMax:
                f.pop(1)
# print(cleaned_faces)

# End the timer
end_time = time.time()
time_taken = end_time - start_time
print(f"Time taken for applying: {time_taken} seconds")
# Start the timer
start_time = time.time()

print("Correcting face indices to remove nan...")
# print("Subtracted and corrected cleaned faces with nans eliminated")
modified_cleaned_faces = nan_correct(cleaned_faces, nan_vertices)
# print(modified_cleaned_faces)

# End the timer
end_time = time.time()
time_taken = end_time - start_time
print(f"Time taken for correcting: {time_taken} seconds")
# Start the timer
start_time = time.time()

print("Creating list of edge vertices...")
# print("Vertices located on the edge")
edge_vertices = sorted(set(sum(modified_cleaned_faces, [])))
# print(edge_vertices)

# End the timer
end_time = time.time()
time_taken = end_time - start_time
print(f"Time taken for creating: {time_taken} seconds")

# OBJ after nan removed
refined_file = filedialog.askopenfilename(filetypes=[("Refined OBJ file", "*.obj")], initialdir=script_directory+'/obj')
print("Refined output:", refined_file)

# Start the timer
start_time = time.time()

print("Counting all vertices...")
floor_v_count = count_vertices(refined_file)

# End the timer
end_time = time.time()
time_taken = end_time - start_time
print(f"Time taken for counting: {time_taken} seconds")

# Combined OBJ
target_file = filedialog.askopenfilename(filetypes=[("Target file", "*.obj")], initialdir=script_directory+'/obj')
print("Target combined:", target_file)

# Write to the output file
obj_output = filedialog.asksaveasfilename(defaultextension='.obj',
                                        filetypes=[('OBJ files', '*.obj')],
                                        title='Save output file as',
                                        initialfile=f'edge_output.obj',
                                        initialdir=script_directory+'/obj')
print("Output:", obj_output)

# Start the timer
start_time = time.time()

print("Writing to a new file...")
with open(target_file, 'r') as target, open(obj_output, 'w') as output:
    # Write all lines
    for line in target:
        output.write(line)

    # Add edge lines
    for v in edge_vertices:
        output.write(' '.join(['l', str(v), str(v+floor_v_count)])+'\n')

# End the timer
end_time = time.time()
time_taken = end_time - start_time
print(f"Time taken for writing: {time_taken} seconds")
