"""
Script to automate camera renders in Blender
Lisa Fung
11/29/2024

Blend file: "./automate_camera_dice.blend"
Goal: automatically render multiple images with different camera orientations 
    Produce baseline drone path: camera moves in horizontal circle with specific radius and height, 
        camera angle always facing origin, specify radian angle to increment, total number of images
"""

import bpy
import math
import os

# Variables to change for each Blender scene
output_path = "C:\\Users\\lisaf\\Documents\\2stanford_year2\\1autumn2024\\CS238\\Final Project\\cs238-nerf-drone-path-planning\\dev_automate_camera_outputs"
camera_xy_radius = 50
camera_z = 37
total_images = 10
angle_increment = 2 * math.pi / total_images

# Set render output path
output_path = output_path.replace("\\", "/")
print("Output path:", output_path)
print("Working directory:", os.getcwd())

# Get the camera object
camera = bpy.context.scene.camera

# Set the render resolution
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080

# Set the camera location
# camera.location = (15.6498, -12.0187, 10.7505)  # Adjust to your scene setup
# camera.rotation_euler = (math.radians(63.5593), 0, math.radians(70))  # Initial rotation

# "Track to" constraint to always point camera at the origin
track_to = camera.constraints.new(type='TRACK_TO')
track_to.target = bpy.data.objects.new("Target", None)  # Create an empty target at the origin
track_to.target.location = (0, 0, 0)
track_to.up_axis = 'UP_Y'
track_to.track_axis = 'TRACK_NEGATIVE_Z'

# Loop through camera positions for circular flight path
for i in range(total_images):
    # Angle with positive x-axis on xy-plane
    angle = angle_increment * i

    # Set the camera's location
    camera.location = (camera_xy_radius * math.cos(angle), camera_xy_radius * math.sin(angle), camera_z)

    # Update the scene
    bpy.context.view_layer.update()

    # Set the output file name
    output_filename = f"{output_path}/circle_dice_r{camera_xy_radius}_z{camera_z}/dice_circle_{i}.png"
    bpy.context.scene.render.filepath = output_filename

    # Render the scene
    bpy.ops.render.render(write_still=True)

    print(f"Rendered image with camera located at {camera.location}.")

print(f"Finished Rendering!")