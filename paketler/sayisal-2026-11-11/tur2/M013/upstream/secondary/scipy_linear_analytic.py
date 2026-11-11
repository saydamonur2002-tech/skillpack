def fun_zero(t, y):
    return np.zeros_like(y)


def fun_linear(t, y):
    return np.array([-y[0] - 5 * y[1], y[0] + y[1]])


def jac_linear():
    return np.array([[-1, -5], [1, 1]])


def sol_linear(t):
    return np.vstack((-5 * np.sin(2 * t),
                      2 * np.cos(2 * t) + np.sin(2 * t)))