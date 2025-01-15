import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import pymc
import bambi as bmb
import arviz


sns.set(style="darkgrid", palette="muted")


def simulate_linear_data(N, beta_0, beta_1, eps_sigma_sq):
    '''
        Generate a random dataset using a noisy linear process
        :param N: number of data point to generate
        :param beta_0: Intercept
        :param beta_1: Slope
        :param eps_sigma_sq: Noise variance
        :return: the generated dataset
    '''

    # Create a dataframe with column x, containing N uniformly samples values in [0.0, 1.0]
    df = pd.DataFrame(
        {
            "x": np.random.RandomState(42).choice(
                list(map(
                    lambda x: float(x) / 100.0,
                    np.arange(100)
                )), N, replace=False
            )
        }
    )

    # Use a linear model (y - beta_0 + beta_1 * x + epsilon) to generate a column y
    eps_mean = 0
    df["y"] = beta_0 + beta_1 * df["x"] + np.random.RandomState(42).normal(eps_mean, eps_sigma_sq, N)

    return df


def glm_mcmc_inference(df, iterations=5000):
    """
        Calculate the MCMC trace of a Generalized Linear Model Bayesian linear regression
        :param df: the data
        :param iterations: number of iterations to carry out MCMC for
        :return:
    """

    model = bmb.Model("y ~ x", df, family="gaussian")
    idata = model.fit(draws=iterations)

    return model, idata


if __name__ == "__main__":
    beta_0 = 1.0
    beta_1 = 2.0

    N = 100
    eps_sigma_sq = 0.5

    df = simulate_linear_data(N, beta_0, beta_1, eps_sigma_sq)

    sns.lmplot(x="x", y="y", data=df)
    plt.xlim(0.0, 1.0)

    plt.show()

    model, trace = glm_mcmc_inference(df, 5000)

    arviz.plot_trace(trace)
    plt.show()

    fig, ax = plt.subplots(figsize=(7, 3), dpi=120)
    bmb.interpret.plot_predictions(model, trace, "x", ax=ax)
