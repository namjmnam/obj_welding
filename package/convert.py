import os
from tkinter import filedialog
from package.utils import get_faces
from package.utils import nan_correct
import time

class Converter:
    def __init__(self) -> None:
        # Get the script directory
        script_directory = os.path.dirname(os.path.abspath(__file__))

        # Get the ceiling obj
        ceil_obj_file = filedialog.askopenfilename(filetypes=[("Ceiling OBJ files", "*.obj")], initialdir=script_directory+'/../obj')
        print(ceil_obj_file)

        # Get the floor obj
        floo_obj_file = filedialog.askopenfilename(filetypes=[("Floo OBJ files", "*.obj")], initialdir=script_directory+'/../obj')
        print(floo_obj_file)

        # Start the timer
        start_time = time.time()

        # Initialize an empty list to hold the line numbers
        self.nan_vertices = []

        print("Fetching all lines with nan...")
        # Get all lines with "nan"
        with open(ceil_obj_file, 'r') as file:
            # Enumerate over each line in the file, starting with line number 1
            for line_number, line in enumerate(file, 1):
                # Check if "nan" is in the line
                if "nan" in line:
                    # Add the line number to the list
                    self.nan_vertices.append(line_number)

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
        self.faces = get_faces(ceil_obj_file)
        # print(faces)

        # End the timer
        end_time = time.time()
        time_taken = end_time - start_time
        print(f"Time taken to fetch: {time_taken} seconds")
        # Start the timer
        start_time = time.time()

        print("Creating a list of faces without nan...")
        # print("Faces without nans")
        filtered_faces = [f for f in self.faces if not any(v in self.nan_vertices for v in f)]
        # print(filtered_faces)

        # End the timer
        end_time = time.time()
        time_taken = end_time - start_time
        print(f"Time taken to create: {time_taken} seconds")
        # Start the timer
        start_time = time.time()

        print("Creating a list of faces on the edge...")
        # print("Faces with nans but not all are nans")
        self.edge_faces = [f for f in self.faces if any(v in self.nan_vertices for v in f) and not all(v in self.nan_vertices for v in f)]
        # print(edge_faces)

        # End the timer
        end_time = time.time()
        time_taken = end_time - start_time
        print(f"Time taken to create: {time_taken} seconds")
        # Start the timer
        start_time = time.time()

        print("Removing all nan from the edges...")
        # print("From edge faces, all nan vertices removed")
        self.cleaned_faces = []
        for f in self.edge_faces:
            # Remove values that are in the first list
            cleaned_list = [value for value in f if value not in self.nan_vertices]
            self.cleaned_faces.append(cleaned_list)
        # print(cleaned_faces)

        # End the timer
        end_time = time.time()
        time_taken = end_time - start_time
        print(f"Time taken to remove: {time_taken} seconds")
        # Start the timer
        start_time = time.time()

        print("Correcting indices of faces with nan eliminated...")
        # print("Subtracted and corrected faces with nans eliminated")
        modified_faces = nan_correct(filtered_faces, self.nan_vertices)
        # print(modified_faces)

        # End the timer
        end_time = time.time()
        time_taken = end_time - start_time
        print(f"Time taken to correct: {time_taken} seconds")
        # Start the timer
        start_time = time.time()

        print("Correcting indices of faces on the edge with nan eliminated...")
        # print("Subtracted and corrected cleaned faces with nans eliminated")
        self.modified_cleaned_faces = nan_correct(self.cleaned_faces, self.nan_vertices)
        # print(modified_cleaned_faces)

        # End the timer
        end_time = time.time()
        time_taken = end_time - start_time
        print(f"Time taken to correct: {time_taken} seconds")
        # Start the timer
        start_time = time.time()

        print("Unpacking list of vertices on the edge...")
        # print("Vertices located on the edge")
        self.edge_vertices = sorted(set(sum(self.modified_cleaned_faces, [])))
        # print(edge_vertices)

        # End the timer
        end_time = time.time()
        time_taken = end_time - start_time
        print(f"Time taken to unpack: {time_taken} seconds")

        # Write to the output file
        ceil_obj_output = filedialog.asksaveasfilename(defaultextension='.obj',
                                                filetypes=[('OBJ files', '*.obj')],
                                                title='Save output file as',
                                                initialfile=f'output_ceil.obj',
                                                initialdir=script_directory+'/../obj')

        # Start the timer
        start_time = time.time()

        print("Writing the ceiling output file...")
        # Delete all lines that contain "nan"
        with open(ceil_obj_file, 'r') as input_file, open(ceil_obj_output, 'w') as output_file:
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
            for f in self.modified_cleaned_faces:
                if len(f)>=3:
                    output_file.write('f '+' '.join(str(num) for num in f)+'\n')

        # End the timer
        end_time = time.time()
        time_taken = end_time - start_time
        print(f"Time taken to rewrite the ceiling: {time_taken} seconds")

        # Write to the output file
        floo_obj_output = filedialog.asksaveasfilename(defaultextension='.obj',
                                                filetypes=[('OBJ files', '*.obj')],
                                                title='Save output file as',
                                                initialfile=f'output_floo.obj',
                                                initialdir=script_directory+'/../obj')

        # Start the timer
        start_time = time.time()

        print("Writing the floor output file...")
        # Delete all lines that contain "nan"
        with open(floo_obj_file, 'r') as input_file, open(floo_obj_output, 'w') as output_file:
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
            for f in self.modified_cleaned_faces:
                if len(f)>=3:
                    output_file.write('f '+' '.join(str(num) for num in f)+'\n')

        # End the timer
        end_time = time.time()
        time_taken = end_time - start_time
        print(f"Time taken to rewrite the floor: {time_taken} seconds")
