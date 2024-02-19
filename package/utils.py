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

def nan_correct(faces, nan_vertices):
    modified_faces = []
    for lst in faces:
        modified_list = []
        for value in lst:
            # Count the number of numbers in the first list that are smaller than the current value
            count_smaller = sum(1 for num in nan_vertices if num < value)
            # Subtract the count from the value
            modified_value = value - count_smaller
            modified_list.append(modified_value)
        modified_faces.append(modified_list)
    return modified_faces

def count_vertices(file_path):
    count = 0
    with open(file_path, 'r') as file:
        for line in file:
            if 'v' in line:
                count += 1
    return count