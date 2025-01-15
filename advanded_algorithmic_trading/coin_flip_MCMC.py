import matplotlib.pyplot as plt
import numpy as np
import pymc
import scipy.stats as stats
from arviz import InferenceData
from pymc.backends.base import MultiTrace

plt.style.use("ggplot")

if __name__ == "__main__":
    n = 50
    z = 10
    alpha = 12
    beta = 12
    alpha_post = 22
    beta_post = 52

    iterations = 1000

    basic_model = pymc.Model()
    with basic_model:
        # Define the prior belief of the coin fairness with a Beta distribution
        theta = pymc.Beta("theta", alpha=alpha, beta=beta)

        # Define the Bernoully likelihood function
        y = pymc.Binomial("y", n=n, p=theta, observed=z)

        # Actual MCMC analysis with Metropolis algorithm

        # Use MAP to find the best initial value
        start = pymc.find_MAP()
        step = pymc.Metropolis()
        trace = pymc.sample(iterations, step=step, start=start, random_seed=1, progressbar=True)

    bins = 50

    plt.hist(
        trace.posterior["theta"][0], bins,
        histtype="step", density=True,
        label="Posterior (MCMC)",
    )

    x = np.linspace(0, 1, 100)
    plt.plot(
        x, stats.beta.pdf(x, alpha, beta),
        "--", label="Prior", color="blue"
    )

    plt.plot(
        x, stats.beta.pdf(x, alpha_post, beta_post),
        label="Posterior (Analytic)", color="green"
    )

    plt.legend(title="Parameters", loc="best")
    plt.xlabel("$\\theta$, Fairness")
    plt.ylabel("Density")
    plt.show()