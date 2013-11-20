#Light field Assignment
#By Abe Davis

import numpy as np
import scipy as sp
from scipy import ndimage

#   ###  *NOTES!*  ###
# Our light fields are to be indexed
# LF[v,u,y,x,color]
#
# Our focal stacks are to be indexed
# FS[image, y, x, color]

def imIter(im):
    for y in xrange(im.shape[0]):
        for x in xrange(im.shape[1]):
            yield (y, x)

def BW2D(im, weights=[0.3, 0.6, 0.1]):  
    out = np.zeros([im.shape[0], im.shape[1]])
    for (y, x) in imIter(out):
        out[y, x] = np.dot(im[y, x], weights)
    return out


def apertureView(LF):
    ''' Takes a light field, returns 'out,' an image with nx*ny sub-pictures representing the value of
        each pixel in each of the nu*nv views.'''
    nv = LF.shape[0]
    nu = LF.shape[1]
    ny = LF.shape[2]
    nx = LF.shape[3]
    out = np.zeros([nv*ny, nu*nx, 3])
    for y in range(ny):
        for x in range(nx):
            for v in range(nv):
                for u in range(nu):
                    out[(y*nv) + v, (x*nu) + u] = LF[v,u,y,x]
    return out


def epiSlice(LF, y):
    '''Takes a light field. Returns the epipolar slice with constant v=(nv/2) and constant y (input argument).'''
    out = np.zeros([LF.shape[1], LF.shape[3], 3])
    out = LF[LF.shape[0]/2, :, y, :, :]
    return out
##    nv = LF.shape[0]
##    nu = LF.shape[1]
##    ny = LF.shape[2]
##    nx = LF.shape[3]
##    out = np.zeros([nu, nx, 3])
##    vO = nv/2
##    for yO in range(out.shape[0]):
##        for x in range(nx):
##            for v in range(nv):
##                for u in range(nu):
##                    out[yO, x] = LF[vO,u,y,x]
##    return out

def shiftFloat(im, dy, dx):
    ''' Returns a copy of im shifted by the floating point values dy in y and dx in x.
        We want this to be fast so use either scipy.ndimage.map_coordinates or
        scipy.ndimage.interpolation.affine_transform.'''
    return ndimage.interpolation.shift(im, [dy, dx, 0], mode='nearest')


def refocusLF(LF, maxParallax=0.0, aperture=17):
    ''' Takes a light field as input and outputs a focused image by summing over u and v with the correct
        shifts applied to each image. Use aperture*aperture views, centered at the center of views in LF.
        A view at the center should not be shifted. Views at opposite ends of the aperture should have shifts
        that differ by maxParallax. See handout for more details.'''
    nv = LF.shape[0]
    nu = LF.shape[1]
    ny = LF.shape[2]
    nx = LF.shape[3]
    centerv = nv/2 #v coordinate of center view
    centeru = nu/2 #u coordinate of center view
    print LF.shape
    out = np.zeros([nv*ny, nu*nx, 3])
    weight_sum = 0
##    for y in range(ny):
##        for x in range(nx):
##            for v in range(nv):
##                for u in range(nu):
##                    shift = shiftFloat(LF[v,u], y, x)
##                    weight_sum += shift
    temp = [x for x in LF[0]]
    print temp[0].shape
    return temp

def rackFocus(LF, aperture=8, nIms = 15, minmaxPara=-7.0, maxmaxPara=2.0):
    '''Takes a light field, returns a focal stack. See handout for more details '''
    out = np.zeros([nIms, LF.shape[2], LF.shape[3], LF.shape[4]])    
    
    return out


def sharpnessMap(im, exponent=1.0, sigma=1.0):
    '''Computes the sharpness map of one image. This will be used when we compute all-focus images. See handout.'''
    lum = np.dot(im, np.array([0.3, 0.6, 0.1]))
    blur = ndimage.filters.gaussian_filter(lum, sigma)
    high = lum - blur
    energy = high*high
    sharpness = ndimage.filters.gaussian_filter(energy, 4 * sigma)
    high_contrast_sharpness = sharpness ** exponent
    out = np.zeros([high_contrast_sharpness.shape[0], high_contrast_sharpness.shape[1], 3])
    for i in xrange(3):
        out[:, :,i] = high_contrast_sharpness
    return out
    
def sharpnessStack(FS, exponent=1.0, sigma=1.0):
    '''This should take a focal stack and return a stack of sharpness maps. We provide this function for you.'''
    SS = np.zeros_like(FS)
    for i in xrange(FS.shape[0]):
        SS[i]=sharpnessMap(FS[i], exponent, sigma)
    return SS


def fullFocusLinear(stack, exponent=1.0, sigma=1.0):
    '''takes a numpy array stack[image, y, x, color] and returns an all-focus image and a depth map. See handout.'''
    out = np.zeros_like(stack[0])
    zmap = np.zeros_like(stack[0])
    SS = sharpnessStack(stack, exponent, sigma)
    weight_sum = np.zeros_like(out)
    for sharp in SS:
        weight_sum += sharp
    for i in range(stack.shape[0]):
        out += stack[i] * SS[i]
        zmap += float(i) / stack.shape[0] * SS[i]
    out /= weight_sum
    zmap /= weight_sum
    zmap = zmap * zmap
    return out, zmap


