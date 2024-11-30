"""
Script to automate camera renders in Blender
Lisa Fung
11/29/2024

Blend file: "./automate_camera_dice.blend"
Goal: automatically render *video* with different camera orientations 
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
# total_images = 10
# angle_increment = 2 * math.pi / total_images

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

# Create an empty target at the origin
target_origin = bpy.data.objects.new("Target", None)  
bpy.context.scene.collection.objects.link(target_origin)  # This line links the target to the scene
target_origin.location = (0, 0, 0)

# "Track to" constraint to always point camera at the origin
track_to = camera.constraints.new(type='TRACK_TO')
track_to.target = target_origin
track_to.up_axis = 'UP_Y'
track_to.track_axis = 'TRACK_NEGATIVE_Z'

# Set the frame rate (optional)
bpy.context.scene.render.fps = 24

# Set the start and end frames for the animation
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 50

# Create the camera motion (circle around the sphere)
num_frames = bpy.context.scene.frame_end - bpy.context.scene.frame_start + 1

for frame in range(bpy.context.scene.frame_start, bpy.context.scene.frame_end + 1):
    # Calculate angle for the circular path
    angle = 2 * math.pi * (frame / num_frames)  # Full rotation in 250 frames
    x = camera_xy_radius * math.cos(angle)
    y = camera_xy_radius * math.sin(angle)
    z = camera_z

    # Set camera location
    camera.location = (x, y, z)

    # Insert keyframes for position and rotation
    camera.keyframe_insert(data_path="location", frame=frame)
    camera.keyframe_insert(data_path="rotation_euler", frame=frame)

# Set the output file name
output_filename = f"{output_path}/circle_dice_r{camera_xy_radius}_z{camera_z}_f{num_frames}.mp4"
bpy.context.scene.render.filepath = output_filename

# Set the render engine
bpy.context.scene.render.engine = 'CYCLES'

# Set render settings for video output
bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
bpy.context.scene.render.ffmpeg.format = 'MPEG4'  # .mp4 format
bpy.context.scene.render.ffmpeg.codec = 'H264'  # Video codec
bpy.context.scene.render.ffmpeg.audio_codec = 'AAC'  # Audio codec (optional)

# Render the animation to a video file
bpy.ops.render.render(animation=True)

print("Animation rendering complete!")