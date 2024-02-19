import os
from tkinter import filedialog

def adjust_face_indices(line, vertex_offset, texture_offset, normal_offset):
    parts = line.split()  # Split the line into parts
    adjusted_parts = [parts[0]]  # The first part is 'f', so keep it as is

    for part in parts[1:]:  # For each part of the face definition (skipping 'f')
        # Split each part by '/' and handle differently based on the count
        sub_parts = part.split('/')
        
        # Reconstruct the face index information based on available data
        if len(sub_parts) == 3:  # v/vt/vn format
            v, vt, vn = sub_parts
            v = str(int(v) + vertex_offset)
            vt = str(int(vt) + texture_offset) if vt else ''
            vn = str(int(vn) + normal_offset) if vn else ''
            adjusted_parts.append('/'.join(filter(None, [v, vt, vn])))
        elif len(sub_parts) == 2:  # v/vt or v//vn format
            v, vt_or_vn = sub_parts
            v = str(int(v) + vertex_offset)
            if '//' in part:  # v//vn format
                vn = str(int(vt_or_vn) + normal_offset)
                adjusted_parts.append(f"{v}//{vn}")
            else:  # v/vt format
                vt = str(int(vt_or_vn) + texture_offset)
                adjusted_parts.append(f"{v}/{vt}")
        elif len(sub_parts) == 1:  # v format
            v = str(int(sub_parts[0]) + vertex_offset)
            adjusted_parts.append(v)
        else:
            raise ValueError(f"Unexpected face definition format: {part}")

    return ' '.join(adjusted_parts)

def combine_obj_files(file1_path, file2_path, output_path):
    """
    Combines two .obj files into a single file.
    """
    # Initialize counters for offsets
    vertex_offset = 0
    texture_offset = 0
    normal_offset = 0
    
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2, open(output_path, 'w') as output_file:
        # Write contents of the first file as is
        for line in file1:
            output_file.write(line)
            if line.startswith('v '):
                vertex_offset += 1
            elif line.startswith('vt '):
                texture_offset += 1
            elif line.startswith('vn '):
                normal_offset += 1
        
        # Process the second file and adjust face indices
        for line in file2:
            if line.startswith('f '):
                # Adjust the face line indices
                adjusted_line = adjust_face_indices(line, vertex_offset, texture_offset, normal_offset)
                output_file.write(adjusted_line + '\n')
            elif not line.startswith(('v ', 'vt ', 'vn ')):
                # Write lines that are not vertices, textures, or normals directly
                output_file.write(line)
            else:
                # For vertices, textures, and normals, just add to the combined file
                output_file.write(line)

script_directory = os.path.dirname(os.path.abspath(__file__))

floo_file = filedialog.askopenfilename(filetypes=[("OBJ floor file", "*.obj")], initialdir=script_directory)
ceil_file = filedialog.askopenfilename(filetypes=[("OBJ ceiling file", "*.obj")], initialdir=script_directory)
combined_file = filedialog.asksaveasfilename(defaultextension='.obj',
                                        filetypes=[('OBJ files', '*.obj')],
                                        title='Save output file as',
                                        initialfile=f'combined.obj',
                                        initialdir=script_directory)

# Example usage
combine_obj_files(floo_file, ceil_file, combined_file)
