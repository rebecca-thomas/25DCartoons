from cartoon import createImage
import sys

if __name__ == '__main__':
    inputFile = sys.argv[1]
    outputBase = sys.argv[2]
    imageAngles = [[0,0,1], [0,1,0], [1,0,0],
                   [0,1,1], [1,1,0], [1,0,1],
                   [0,0,-1], [0,-1,0], [-1,0,0],
                   [0,-1,-1], [-1,-1,0], [-1,0,-1],
                   [0,-1,1], [-1,1,0], [-1,0,1],
                   [0,1,-1], [1,-1,0], [1,0,-1]]

    print len(imageAngles)
    
    for i in range(0, len(imageAngles)):
        print "creating image: ", i
        createImage(inputFile, outputBase + ''.join(map(str, imageAngles[i])) + '.svg', imageAngles[i])
