import os
from tkinter import filedialog
from package.utils import get_faces
from package.utils import nan_correct

# Get the script directory
script_directory = os.path.dirname(os.path.abspath(__file__))

obj_file = filedialog.askopenfilename(filetypes=[("OBJ files", "*.obj")], initialdir=script_directory+'/obj')

# Initialize an empty list to hold the line numbers
nan_vertices = []

# Get all lines with "nan"
with open(obj_file, 'r') as file:
    # Enumerate over each line in the file, starting with line number 1
    for line_number, line in enumerate(file, 1):
        # Check if "nan" is in the line
        if "nan" in line:
            # Add the line number to the list
            nan_vertices.append(line_number)

# print("All nans")
# print(nan_vertices)

# Get all lists of faces
faces = get_faces(obj_file)
# print(faces)

# print("Faces without nans")
filtered_faces = [f for f in faces if not any(v in nan_vertices for v in f)]
# print(filtered_faces)

# print("Faces with nans but not all are nans")
edge_faces = [f for f in faces if any(v in nan_vertices for v in f) and not all(v in nan_vertices for v in f)]
# print(edge_faces)

# print("From edge faces, all nan vertices removed")
cleaned_faces = []
for f in edge_faces:
    # Remove values that are in the first list
    cleaned_list = [value for value in f if value not in nan_vertices]
    cleaned_faces.append(cleaned_list)
# print(cleaned_faces)

# print("Subtracted and corrected faces with nans eliminated")
modified_faces = nan_correct(filtered_faces, nan_vertices)
# print(modified_faces)

# print("Subtracted and corrected cleaned faces with nans eliminated")
modified_cleaned_faces = nan_correct(cleaned_faces, nan_vertices)
# print(modified_cleaned_faces)

# Write to the output file
obj_output = filedialog.asksaveasfilename(defaultextension='.obj',
                                        filetypes=[('OBJ files', '*.obj')],
                                        title='Save output file as',
                                        initialfile=f'output.obj',
                                        initialdir=script_directory+'/obj')

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
    # Needs improvement, because it should not add bottomleft-topright triangles?
    for f in modified_cleaned_faces:
        if len(f)>=3:
            output_file.write('f '+' '.join(str(num) for num in f)+'\n')
