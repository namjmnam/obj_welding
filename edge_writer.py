import os
from tkinter import filedialog
from package.utils import get_faces
from package.utils import nan_correct
from package.utils import count_vertices

# Get the script directory
script_directory = os.path.dirname(os.path.abspath(__file__))

obj_file = filedialog.askopenfilename(filetypes=[("Original floor or celing OBJ file", "*.obj")], initialdir=script_directory+'/obj')

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

# Get all lists of faces
faces = get_faces(obj_file)
# print(faces)

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

# print("Subtracted and corrected cleaned faces with nans eliminated")
modified_cleaned_faces = nan_correct(cleaned_faces, nan_vertices)
# print(modified_cleaned_faces)

# print("Vertices located on the edge")
edge_vertices = sorted(set(sum(modified_cleaned_faces, [])))
# print(edge_vertices)

# OBJ after nan removed
refined_file = filedialog.askopenfilename(filetypes=[("Refined OBJ file", "*.obj")], initialdir=script_directory+'/obj')
floor_v_count = count_vertices(refined_file)

# Combined OBJ
target_file = filedialog.askopenfilename(filetypes=[("Target file", "*.obj")], initialdir=script_directory+'/obj')

# Write to the output file
obj_output = filedialog.asksaveasfilename(defaultextension='.obj',
                                        filetypes=[('OBJ files', '*.obj')],
                                        title='Save output file as',
                                        initialfile=f'edge_output.obj',
                                        initialdir=script_directory+'/obj')

with open(target_file, 'r') as target, open(obj_output, 'w') as output:
    # Write all lines
    for line in target:
        output.write(line)

    # Add edge lines
    for v in edge_vertices:
        output.write(' '.join(['l', str(v), str(v+floor_v_count)])+'\n')

# 삼각형에 대한 고찰
# 삼각형이 어느 대각선을 가지고 있는지, 어느 방향인지
# 삼각형일 경우 대각선만 edge로 만들기
# 예: 1 2 12 11 (xmax = 10)
# 좌상: 1 2 11 - 1과 2가 1 차이인 경우 + 1과 3이 10차이인 경우: 1번째 제거
# 우상: 1 2 12 - 1과 2가 1 차이인 경우 + 1과 3이 11차이인 경우: 2번째 제거
# 좌하: 1 12 11 - 2와 3이 1 차이인 경우 + 1과 2가 11차이인 경우: 3번째 제거
# 우하: 2 12 11 - 2와 3이 1 차이인 경우 + 1과 2가 10차이인 경우: 2번째 제거
