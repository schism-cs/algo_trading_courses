import numpy as np
from scipy import stats
from matplotlib import pyplot as plt

if __name__ == "__main__":
    number_of_trials = [0, 2, 10, 50, 500, 1000]

    # Collect the 500 coin tosses
    data = stats.bernoulli.rvs(0.5, size=number_of_trials[-1])

    # Discretize x-axis in 100 separate plottin points
    x = np.linspace(0, 1, 100)

    for i, N, in enumerate(number_of_trials):
        heads = data[:N].sum()

        ax = plt.subplot(int(len(number_of_trials) / 2), 2, i + 1)
        ax.set_title(f"{N} trials, {heads} heads")

        plt.xlabel("$P(H)$, Probability of Heads")
        plt.ylabel("Density")

        if i == 0:
            plt.ylim([0.0, 2.0])
        plt.setp(ax.get_yticklabels(), visible=False)

        y = stats.beta.pdf(x, 1 + heads, 1 + N - heads)
        plt.plot(x, y, label=f"observe {N} tosses with {heads} heads")
        plt.fill_between(x, 0, y, color="#aaaadd", alpha=0.5)

    plt.tight_layout()
    plt.show()