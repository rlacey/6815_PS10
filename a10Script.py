#a10Script.py
#hacked together by Abe
import numpy as np
import a10 as lf
import imageIO as io
import math
io.baseInputPath = './'

test = np.zeros([100,100,3])
test[:,:50] = 1
test[25,:] = 1
io.imwrite(test, 'test.png')
a = lf.shiftFloat(test, 25, 0)
io.imwrite(a, 'test_shifted.png')

##This assumes that you unzip the chessNumpy.zip into the same directory
##chess3x3 = np.load('./input/chess/chess3x3.npy')
##chess5x5 = np.load('./input/chess/chess5x5.npy')
##chess17x17 = np.load('./input/chess/chess17x17.npy')

bugStack = np.load('./input/BugStack.npy')
##lytro1 = np.load('./input/counter1.npy')

def testApertureView(LF, outname):
    io.imwrite(lf.apertureView(LF), outname+'.png')

def testEpiSlice(LF, y, outname):
    io.imwrite(lf.epiSlice(LF, y), outname+'.png')

def testRefocusLF(LF, focus, outname):
    aperture = LF.shape[0]
    l = lf.refocusLF(LF, focus, aperture)
    for i in range(len(l)):
        io.imwrite(l[i], outname+str(i)+'.png')
##    io.imwrite(lf.refocusLF(LF, focus, aperture), outname+'.png')

def testRackFocus(LF, outname, nIms = 15, minPar=-7.0, maxPar=2.0):
    aperture = LF.shape[0]
    fstack = lf.rackFocus(LF, aperture, nIms, minPar, maxPar)
    fullname = outname+'_min'+str(minPar)+'_max'+str(maxPar)+'nIms_'+str(nIms)
    printFocalStack(fstack, fullname+'_')
    return fstack, fullname
        

def printFocalStack(FS, outname):
    for i in xrange(FS.shape[0]):
        io.imwrite(FS[i], outname+str(i)+'.png')

def saveNP(A, outname):
    np.save('./myLFs/'+outname+'.npy', A)

def printSharpnessStack(FS, outname):
    printFocalStack(lf.sharpnessStack(FS), outname)

def testFullFocusLinear(FS, outname, exponent=3.0, sigma=1.0):
    allfocus, depthmap = lf.fullFocusLinear(FS, exponent, sigma)
    io.imwrite(allfocus, outname+'AllFocus.png')
    io.imwrite(depthmap, outname+'DepthMap.png')

##for i in xrange(chess5x5.shape[1]):
##    print chess5x5.shape
##    print chess5x5[1][i].shape    
##    sharp = lf.sharpnessMap(chess5x5[0][i])
##    print 'sharp', sharp.shape
##    io.imwrite(sharp, 'sharp'+str(i)+'.png')    

##testApertureView(chess3x3, "chess3x3ApertureViews")
##testApertureView(chess5x5, "chess5x5ApertureViews")
##testApertureView(chess17x17, "chess17x17ApertureViews")
##testEpiSlice(chess17x17, 100, "chess17x17Epislicey100")
##testRefocusLF(chess5x5, 0.0, "chess5x5Focus0")
##testRefocusLF(chess17x17, 0.0, "chess17x17Focus0")

#chessStack17, chessStack17Name = testRackFocus(chess17x17, "chess17x17_new")
#saveNP(chessStack17, chessStack17Name)

##chessStack17 = np.load('myLFs/chess17x17_min-7.0_max2.0nIms_15.npy')
#printFocalStack(chessStack17, "testChessStack")
##printSharpnessStack(chessStack17, 'testChessSharpness')
#testFullFocusLinear(chessStack17, "chessStack17")
##printSharpnessStack(bugStack, 'testBugSharpness')
testFullFocusLinear(bugStack, "bugStack")

#testFullFocusLinear(bugStack, "bugStack")
#testFullFocusLinear(lytro1, "lytro1")
