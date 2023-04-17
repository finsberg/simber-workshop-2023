import numpy as np
import matplotlib.pyplot as plt


def arrow_annotate(axi, y, t1, t2, label):
    mid_t = 0.5 * (t1 + t2)
    axi.annotate(
        text="",
        xy=(t1, y),
        xytext=(t2, y),
        arrowprops=dict(arrowstyle="<->"),
    )
    axi.text(
        mid_t,
        y,
        label,
        size="large",
        bbox=dict(boxstyle="circle", fc="w", ec="k"),
    )


def normalize(y):
    return (y - np.min(y)) / (np.max(y) - np.min(y))


def adjust_spines(ax, spines):
    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(("outward", 10))  # outward by 10 points
        else:
            spine.set_color("none")  # don't draw spine

    # turn off ticks where there is no spine
    if "left" in spines:
        ax.yaxis.set_ticks_position("left")
    else:
        # no yaxis ticks
        ax.yaxis.set_ticks([])

    if "bottom" in spines:
        ax.xaxis.set_ticks_position("bottom")
    else:
        # no xaxis ticks
        ax.xaxis.set_ticks([])


def plot_features(u_norm, v_norm, time, start=40, end=100, indices=None):
    if indices is None:
        indices = [7, 16, 31, 43, 56]
    spacing = len(u_norm) - len(v_norm)

    fig, ax = plt.subplots(2, 1, sharex="col", figsize=(12, 6))

    labels = ["1", "2", "3", "4", "5"]

    max_u = np.max(u_norm[start:end]) - np.min(u_norm[start:end])
    max_v = np.max(v_norm[start:end]) - np.min(v_norm[start : end - spacing])

    u_norm = normalize(u_norm[start:end])
    v_norm = normalize(v_norm[start : end - spacing])
    time = normalize(time[start:end])
    time_v = time[spacing // 2 : -spacing // 2]

    indices_v = [i - spacing // 2 for i in indices]

    ax[0].plot(time, u_norm, linewidth=3)

    for ind, label in zip(indices, labels):
        ax[0].text(
            time[ind],
            u_norm[ind],
            label,
            size="large",
            bbox=dict(boxstyle="circle", fc="w", ec="k"),
        )

    ax[1].plot(time_v[: len(v_norm)], v_norm, linewidth=3)
    for ind, label in zip(indices_v, labels):
        ax[1].text(
            time_v[ind],
            v_norm[ind],
            label,
            size="large",
            bbox=dict(boxstyle="circle", fc="w", ec="k"),
        )

    # Beat duratiom
    arrow_annotate(
        ax[0],
        y=0,
        t1=time[indices[0]],
        t2=time[indices[4]],
        label="6",
    )

    # Time to peak twich amplitude
    ax[0].plot(
        [time[indices[2]], time[indices[2]]],
        [u_norm[indices[2]], 0.7],
        "k:",
    )
    arrow_annotate(
        ax[0],
        y=0.7,
        t1=time[indices[0]],
        t2=time[indices[2]],
        label="7",
    )

    # Time to peak contraction
    ax[1].plot(
        [time_v[indices_v[1]], time_v[indices_v[1]]],
        [v_norm[indices_v[1]], 0.3],
        "k:",
    )
    arrow_annotate(
        ax[1],
        y=0.3,
        t1=time_v[indices_v[0]],
        t2=time_v[indices_v[1]],
        label="8",
    )

    # Time_v to peak relaxation
    ax[1].plot(
        [time_v[indices_v[3]], time_v[indices_v[3]]],
        [v_norm[indices_v[3]], 0.5],
        "k:",
    )
    arrow_annotate(
        ax[1],
        y=0.5,
        t1=time_v[indices_v[0]],
        t2=time_v[indices_v[3]],
        label="9",
    )
    (zero_crossings,) = np.where(np.diff(np.sign(u_norm - 0.5)))

    arrow_annotate(
        ax[0],
        y=0.5,
        t1=time[zero_crossings[0]],
        t2=time[zero_crossings[1]],
        label="10",
    )

    adjust_spines(ax[0], ["left"])
    adjust_spines(ax[1], ["left", "bottom"])

    num_points = 5
    points = np.linspace(0, 1, num_points)
    u_points = np.linspace(0, max_u, num_points)
    ax[0].set_yticks(points)
    ax[0].set_yticklabels([f"{vi:.1f}" for vi in u_points])
    v_points = np.linspace(0, max_v, num_points)
    ax[1].set_yticks(points)
    ax[1].set_yticklabels([f"{vi:.0f}" for vi in v_points])

    t_points = np.linspace(time[0], time[-1], num_points)
    ax[1].set_xticks(points)
    ax[1].set_xticklabels([f"{vi:.0f}" for vi in t_points])
    ax[1].set_xlabel("Time [ms]")

    for axi in ax.flatten():
        axi.grid()

    ax[0].set_ylabel("Displacement [\u00B5m]")
    ax[1].set_ylabel("Velocity [\u00B5m / s]")

    legend = "\n".join(
        [
            "1. Start of beat",
            "2. Maximum rise velocity",
            "3. Peak twitch amplitude",
            "4. Maximum relaxation velocity",
            "5. End of beat",
            "6. Beat duration",
            "7. Time to peak twitch amplitude",
            "8. Time to peak contraction velocity",
            "9. Time to peak relaxation velocity",
            "10. Width at half height",
        ]
    )
    fig.text(0.68, 0.45, legend, size="xx-large")
    fig.subplots_adjust(right=0.65)
    return fig, ax


if __name__ == "__main__":
    d = np.load("d.npy", allow_pickle=True).item()
    plot_features(**d)
    plt.show()
