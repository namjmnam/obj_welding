import os
from tkinter import filedialog
from package.utils import get_faces
from package.utils import nan_correct
from package.utils import count_vertices
from package.convert import Converter
from package.weld import Welder
import time

a = Converter()
b = Welder()

# Get the script directory
script_directory = os.path.dirname(os.path.abspath(__file__))

# Needed for triangles
xMax = 50

# Start the timer
start_time = time.time()

print("Applying triangles algorithm...")
# Now, triangles algorithm
for f in a.cleaned_faces:
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
modified_cleaned_faces = nan_correct(a.cleaned_faces, a.nan_vertices)
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
with open(b.combined_file, 'r') as target, open(obj_output, 'w') as output:
    # Write all lines
    for line in target:
        output.write(line)

    # Add edge lines
    for v in edge_vertices:
        output.write(' '.join(['l', str(v), str(v+b.floor_v_count)])+'\n')

# End the timer
end_time = time.time()
time_taken = end_time - start_time
print(f"Time taken for writing: {time_taken} seconds")

