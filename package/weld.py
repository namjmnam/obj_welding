import os
from tkinter import filedialog
from package.utils import get_faces
from package.utils import count_vertices
import time

class Welder:
    def __init__(self) -> None:
        script_directory = os.path.dirname(os.path.abspath(__file__))

        floo_file = filedialog.askopenfilename(filetypes=[("OBJ floor file", "*.obj")], initialdir=script_directory+'/../obj')
        print("Floor:", floo_file)
        ceil_file = filedialog.askopenfilename(filetypes=[("OBJ ceiling file", "*.obj")], initialdir=script_directory+'/../obj')
        print("Ceiling:", ceil_file)
        self.combined_file = filedialog.asksaveasfilename(defaultextension='.obj',
                                                filetypes=[('OBJ files', '*.obj')],
                                                title='Save output file as',
                                                initialfile=f'combined.obj',
                                                initialdir=script_directory+'/../obj')
        print("Output:", self.combined_file)

        # Start the timer
        start_time = time.time()

        print("Getting floor faces...")
        floo_faces = get_faces(floo_file)
        print("Getting ceiling faces...")
        ceil_faces = get_faces(ceil_file)
        print("Counting vertices...")
        self.floor_v_count = count_vertices(floo_file)
        print("Adjusting ceiling faces indices for stacking...")
        adjusted_ceil_faces = [[num + self.floor_v_count for num in f] for f in ceil_faces]

        # End the timer
        end_time = time.time()
        time_taken = end_time - start_time
        print(f"Time taken for preparation: {time_taken} seconds")
        # Start the timer
        start_time = time.time()

        print("Writing to a new output file...")
        with open(floo_file, 'r') as floo, open(ceil_file, 'r') as ceil, open(self.combined_file, 'w') as output:
            print("Stacking two vertices...")
            for line in floo:
                if "v" in line:
                    output.write(line)
            for line in ceil:
                if "v" in line:
                    output.write(line)

            # Add floor face lines
            print("Adding floor faces...")
            for f in floo_faces:
                output.write('f '+' '.join(str(num) for num in f)+'\n')

            # Add ceiling face lines with adjustment
            print("Adding ceiling faces...")
            for f in adjusted_ceil_faces:
                output.write('f '+' '.join(str(num) for num in f)+'\n')

        # End the timer
        end_time = time.time()
        time_taken = end_time - start_time
        print(f"Time taken to write: {time_taken} seconds")
