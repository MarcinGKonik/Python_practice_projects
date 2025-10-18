import numpy as np

def triangulate(mic_positions, source_directions):
    """
    Triangulates the 3D position of a sound source using a least-squares algorithm.

    Args:
        mic_positions (list of tuples): A list of 3D coordinates for each microphone.
        source_directions (list of tuples): A list of 3D direction vectors for the sound source from each microphone.

    Returns:
        numpy.ndarray: The estimated 3D position of the sound source.
    """
    A = np.zeros((3, 3))
    b = np.zeros(3)

    for i in range(len(mic_positions)):
        p = np.array(mic_positions[i])
        d = np.array(source_directions[i])
        d = d / np.linalg.norm(d)  # Normalize the direction vector

        A += np.eye(3) - np.outer(d, d)
        b += (np.eye(3) - np.outer(d, d)) @ p

    position = np.linalg.solve(A, b)
    return position

if __name__ == '__main__':
    # Dummy data for demonstration
    mic_positions = [
        (0, 0, 0),
        (1, 0, 0),
        (0, 1, 0),
        (1, 1, 0)
    ]

    # These directions would be extracted from the ODAS msg_pots_obj
    source_directions = [
        (1, 1, 1),
        (0, 1, 1),
        (1, 0, 1),
        (0, 0, 1)
    ]

    estimated_position = triangulate(mic_positions, source_directions)
    print(f"Estimated position: {estimated_position}")
