import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define your custom probability function
def gaussian(x):
    mean = 30
    sigma = 20
    return 0.3 * np.exp(-(x-mean)**2 / sigma**2)  # Example: a Gaussian-like shape

def leadpt_pdf(x,mu,sigma,alpha,n):
    # Calculate the Gaussian core and tails
    A = (n / abs(alpha)) ** n * np.exp(-alpha**2 / 2)
    B = n / abs(alpha) - abs(alpha)
    
    # Gaussian core condition
    gauss = np.exp(-(x - mu)**2 / (2 * sigma**2))
    # Power-law tail condition
    tail = A * (B - (x - mu) / sigma) ** -n

    # Apply conditions for piecewise definition
    core_condition = (x - mu) / sigma > -alpha
    return np.where(core_condition, gauss, tail)

# Generate samples from the desired distribution
def generate_samples(pdf,mu,sigma,alpha,n,x_min,x_max,num_samples):
    samples = []
    while len(samples) < num_samples:
        x = np.random.uniform(x_min, x_max)
        y = np.random.uniform(0, 1)
        if y < pdf(x,mu,sigma,alpha,n):
            samples.append(x)
    return np.array(samples)

# Generate samples based on the PDF
num_samples = 10000
xlow = 10
xhigh = 500
#Electron_pT_1 = generate_samples(leadpt_pdf,30,-5,1,10,xlow,xhigh,num_samples)
Electron_pT_2 = generate_samples(leadpt_pdf,20,-10,1,10,xlow,xhigh,num_samples)

plt.hist(Electron_pT_2,bins=50,edgecolor='black')
plt.show()
