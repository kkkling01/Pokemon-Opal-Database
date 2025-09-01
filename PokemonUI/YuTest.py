import cv2

if __name__ == '__main__':

    print(cv2.__version__)

    img = cv2.imread("E:/pokemonIcon/0001.png", cv2.IMREAD_UNCHANGED)
    height, width, channel = img.shape

    fourcc = cv2.VideoWriter.fourcc(*'X264')
    video_writer = cv2.VideoWriter("./pokeIcon.mkv", fourcc, 30, (width, height))

    for i in range(1008):
        img = cv2.imread("E:/pokemonIcon/" + str(i+1).zfill(4) + ".png", cv2.IMREAD_UNCHANGED)
        video_writer.write(img)

    video_writer.release()
