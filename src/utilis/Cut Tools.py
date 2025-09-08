from PIL import Image

sprite = Image.open("../../../../../新建文件夹/GitHub/pet-game/assets/animations/loading/cat_9_0.png")
frame_w, frame_h = 32,32
columns = sprite.width // frame_w
rows = sprite.height // frame_h

count = 0
for y in range(rows):
    for x in range(columns):
        left = x * frame_w
        upper = y * frame_h
        right = left + frame_w
        lower = upper + frame_h
        frame = sprite.crop((left, upper, right, lower))
        frame.save(f"load_frame_{count + 1:02d}.png")
        count += 1

print("done",count,"帧")