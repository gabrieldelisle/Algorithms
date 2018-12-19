from matplotlib.image import imread,imsave
import numpy as np


def rgbToGray(image) :
	return np.sum(image,axis=2)/3

def negative(image) :
	return 1-image

def smooth(image, n=1) :
	image2=image
	for i in range(n):
		image2 = np.concatenate( 
			(( image2[:1,:] + image2[1:2,:] ) / 2,
			( image2[2:,:] + image2[1:-1,:]*2 + image2[:-2,:] ) / 4,
			( image2[-1:,:] + image2[-2:-1,:] ) / 2 ), axis=0)

		image2 = np.concatenate( 
			(( image2[:,:1] + image2[:,1:2] ) / 2,
			( image2[:,2:] + image2[:,1:-1]*2 + image2[:,:-2] ) / 4,
			( image2[:,-1:] + image2[:,-2:-1] ) / 2 ), axis=1)
	return image2


def laplacian(image) :
	return  np.concatenate( 
		(( image[:1,:] - 2 * image[1:2,:] + image[2:3,:] ) / 2,
		( image[2:,:] - 2 * image[1:-1,:] + image[:-2,:] ) / 2,
		( image[-1:,:] - 2 * image[-2:-1,:] + image[-3:-2,:] ) /2 ), axis=0) + np.concatenate( 
		(( image[:,:1] - 2 * image[:,1:2] + image[:,2:3] ) / 2,
		( image[:,2:] - 2 * image[:,1:-1] + image[:,:-2] ) / 2,
		( image[:,-1:] - 2 * image[:,-2:-1] + image[:,-3:-2] ) / 2 ), axis=1)

def border(image) :
	return np.clip(image-laplacian(image),0,1)

def contrast(image, p=None) :
	if p:
		return np.clip((image-0.5)*p+0.5,0,1)
	else:
		a = image.min()
		b = image.max()
		m = (b+a)/2
		return (image-m)*2/(b-a)+m

def diffusion(image, K=1, n=1) :
	image2=image.copy()
	for i in range(n) :
		dx,dy = grad(image)
		c = np.exp(-(dx**2+dy**2)/K**2)
		cx,cy = grad(c)
		image2 + cx*dx + cy*dy + c*laplacian(image2)
	return np.clip(image2 ,0,1)

def colors(image, n) :
	n-=1
	return (image*n**2+n/2)//n/n

def resize(image, N, M) :
	A,B = image.shape[:2]
	a,b = A/N,B/M
	return np.concatenate([np.concatenate([np.array([[np.mean(image[int(i*a):int((i+1)*a), int(j*b):int((j+1)*b)])]]) for i in range(N)], axis=0) for j in range(M)], axis=1)

def filtre(image,a=0,b=float('inf')) :
	#fourier transform
	f = np.fft.fft2(image)

	N,M = f.shape
	f2 = f.copy()
	a*=a
	b*=b
	for i in range(N) :
		for j in range(M):
			d=i**2+j**2
			if d<a or d>b :
				f2[i,j]=0
	return np.abs(np.fft.ifft2(f2))

def phase(image) :
	f = np.fft.fft2(image)
	return np.abs(np.fft.ifft2(f/abs(f)))

if __name__ == '__main__':
	
	image = imread("other/test.png")[:,:,:3]
	grey = rgbToGray(image)
	lap = np.clip(grey-laplacian(grey),0,1)
	smooth = smooth(grey, n=10)
	imsave("other/grey.png", grey, cmap="gray")
	imsave("other/lap.png", lap, cmap="gray")
	imsave("other/smooth.png", smooth, cmap="gray")

	f = np.fft.fft2(grey)
	fshift = np.fft.fftshift(f)

	imsave("other/fourier.png", np.log(np.abs(fshift)), cmap="gray")
	imsave("other/phase.png", phase(grey), cmap="gray")


	M,N=f.shape
	high = filtre(grey,a=3*M/4)
	low = filtre(grey,b=M)
	imsave("other/low.png", low, cmap="gray")
	imsave("other/high.png", border(high), cmap="gray")
	imsave("other/small.png", resize(grey, M//2,N//2), cmap="gray")

