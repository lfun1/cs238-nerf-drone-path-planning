"""
Script to automate camera renders in Blender
Lisa Fung
11/26/2024

Blend file: "./automate_camera_dice.blend"
Goal: automatically render multiple images with different camera orientations 
    Rotate camera from z = 70 degrees to z = 25 degrees, decrement by 5 degrees each time
"""

import bpy
import math
import os

# Set render output path
output_path = "output_path"
output_path = output_path.replace("\\", "/")
print("Output path:", output_path)
print("Working directory:", os.getcwd())

# Get the camera object
camera = bpy.context.scene.camera

# Set the render resolution (adjust if necessary)
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080

# Set the camera location (ensure it is set properly)
camera.location = (15.6498, -12.0187, 10.7505)  # Adjust to your scene setup
camera.rotation_euler = (math.radians(63.5593), 0, math.radians(70))  # Initial rotation

# Loop through the rotation values (70, 65, ..., 25 degrees)
for angle in range(70, 24, -5):
    # Set the camera's Z-axis rotation
    camera.rotation_euler[2] = math.radians(angle)

    # Update the scene
    bpy.context.view_layer.update()

    # Set the output file name
    output_filename = f"{output_path}/z_rot{angle}.png"
    bpy.context.scene.render.filepath = output_filename

    # Render the scene
    bpy.ops.render.render(write_still=True)

    print(f"Rendered image with camera angle {angle} degrees.")
