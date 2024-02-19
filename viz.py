import os
from tkinter import filedialog
import vtk

def visualize_obj(file_path):
    # Create a reader for the .obj file
    reader = vtk.vtkOBJReader()
    reader.SetFileName(file_path)
    reader.Update()

    # Create a mapper for the geometry
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    # Create an actor to hold the geometry
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # Create a renderer and add the actor to it
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(0.1, 0.2, 0.4)  # Set background color

    # Create a render window
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window.SetWindowName("OBJ Viewer")

    # Create a render window interactor
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    # Initialize the interactor and start the rendering loop
    render_window.Render()
    interactor.Initialize()
    interactor.Start()

def get_faces(file_path):
    faces = []  # Initialize an empty list to store faces

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('f '):  # Check if the line defines a face
                # Extract the parts of the line after "f "
                face_line = line.strip().split(' ')[1:]
                
                # For each part, split by '/' and take the first element (vertex index),
                # then convert it to an integer. This ignores texture and normal indices.
                face_vertices = [int(part.split('/')[0]) for part in face_line]
                
                # Add the list of vertex indices to the faces list
                faces.append(face_vertices)

    return faces

# visualize_obj(obj_file)

# Get the script directory
script_directory = os.path.dirname(os.path.abspath(__file__))

obj_file = filedialog.askopenfilename(filetypes=[("OBJ files", "*.obj")], initialdir=script_directory)
obj_output = filedialog.asksaveasfilename(defaultextension='.obj',
                                        filetypes=[('OBJ files', '*.obj')],
                                        title='Save output file as',
                                        initialfile=f'output.obj',
                                        initialdir=script_directory)

# Delete all lines that contain "nan"
with open(obj_file, 'r') as input_file, open(obj_output, 'w') as output_file:
    # Iterate over each line in the original file
    for line in input_file:
        # If "nan" is not found in the line, write it to the new file
        if "nan" not in line and "f" not in line:
            output_file.write(line)

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
# edge_faces = [f for f in faces if any(v in nan_vertices for v in f) and not all(v in nan_vertices for v in f)]
# print(edge_faces)

# print("Subtracted and corrected faces with nans eliminated")
modified_faces = []
for lst in filtered_faces:
    modified_list = []
    for value in lst:
        # Count the number of numbers in the first list that are smaller than the current value
        count_smaller = sum(1 for num in nan_vertices if num < value)
        # Subtract the count from the value
        modified_value = value - count_smaller
        modified_list.append(modified_value)
    modified_faces.append(modified_list)
# print(modified_faces)

# Add new face lines to the output file from above
with open(obj_output, 'a') as output_file:
    for f in modified_faces:
        # print('f '+' '.join(str(num) for num in f)) 
        output_file.write('f '+' '.join(str(num) for num in f)+'\n')
