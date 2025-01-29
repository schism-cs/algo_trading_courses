import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import t

if __name__ == "__main__":
    sns.set_palette("deep", desat=0.6)
    sns.set_context(rc={"figure.figsize": (8, 4)})

    x = np.linspace(-5.0, 5.0, 100)
    nus = [1.0, 2.0, 5.0, 50.0]

    for nu in nus:
        y = t.pdf(x, nu)
        ax = plt.plot(x, y, label="$\\nu=%s$" % nu)

    plt.title("Student's t-distribution")
    plt.xlabel("x")
    plt.ylabel("P(x)")
    plt.legend(title="Parameters")

    plt.show()