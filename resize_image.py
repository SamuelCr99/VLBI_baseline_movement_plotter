from PIL import Image

image = Image.open('world_map.png')
print(f"Original size : {image.size}")

sunset_resized = image.resize((1000, 500))
sunset_resized.save('world_map_smaller.png')
