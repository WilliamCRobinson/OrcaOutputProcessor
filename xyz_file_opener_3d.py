import os
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
from PIL import Image
import imageio

"""
This module is a mess. Not a totally necessary file, but it is handy. 
"""

def generate_rotating_frames(molecule, output_folder, num_frames=36):
    frames = []

    for i in range(num_frames):
        AllChem.Compute2DCoords(molecule)
        AllChem.EmbedMolecule(molecule, randomSeed=i)
        img = Draw.MolToImage(molecule, size=(300, 300), kekulize=False, wedgeBonds=True)
        frames.append(img.rotate(i * (360 / num_frames)))

    # Save frames as individual images
    for i, frame in enumerate(frames):
        img_path = os.path.join(output_folder, f"frame_{i:03d}.png")
        frame.save(img_path)

def create_gif(input_folder, output_gif):
    frames = []
    for filename in sorted(os.listdir(input_folder)):
        if filename.endswith('.png'):
            frames.append(imageio.imread(os.path.join(input_folder, filename)))

    imageio.mimsave(output_gif, frames, duration=0.1)

def main():
    xyz_files_directory = 'C:\\Users\\w62d765\\PycharmProjects\\OrcaOutputProcessor\\xyzdata'
    output_folder = 'output_frames'
    output_gif = 'output_rotating_molecule.gif'

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    xyz_files = [f for f in os.listdir(xyz_files_directory) if f.endswith('.xyz')]

    for xyz_file in xyz_files:
        xyz_path = os.path.join(xyz_files_directory, xyz_file)
        molecule = Chem.MolFromXYZFile(xyz_path)

        # Generate rotating frames
        generate_rotating_frames(molecule, output_folder)

    # Create GIF from frames
    create_gif(output_folder, output_gif)

    print(f"GIF created: {output_gif}")

if __name__ == "__main__":
    main()`
