import os
from tkinter import filedialog
from package.utils import get_faces
from package.utils import count_vertices

script_directory = os.path.dirname(os.path.abspath(__file__))

floo_file = filedialog.askopenfilename(filetypes=[("OBJ floor file", "*.obj")], initialdir=script_directory+'/obj')
ceil_file = filedialog.askopenfilename(filetypes=[("OBJ ceiling file", "*.obj")], initialdir=script_directory+'/obj')
combined_file = filedialog.asksaveasfilename(defaultextension='.obj',
                                        filetypes=[('OBJ files', '*.obj')],
                                        title='Save output file as',
                                        initialfile=f'combined.obj',
                                        initialdir=script_directory+'/obj')

floo_faces = get_faces(floo_file)
ceil_faces = get_faces(ceil_file)
floor_v_count = count_vertices(floo_file)
adjusted_ceil_faces = [[num + floor_v_count for num in f] for f in ceil_faces]

with open(floo_file, 'r') as floo, open(ceil_file, 'r') as ceil, open(combined_file, 'w') as output:
    for line in floo:
        if "v" in line:
            output.write(line)
    for line in ceil:
        if "v" in line:
            output.write(line)

    # Add floor face lines
    for f in floo_faces:
        output.write('f '+' '.join(str(num) for num in f)+'\n')

    # Add ceiling face lines with adjustment
    for f in adjusted_ceil_faces:
        output.write('f '+' '.join(str(num) for num in f)+'\n')
