# Método de Euler
def Euler(f, a, b, c0, h):
    n = int((b - a) / h)
    t = np.linspace(a, b, n + 1)
    yeu = [c0]
    for i in range(n):
        yeu.append(yeu[i] + h * f(t[i], yeu[i])) # reemplazar aqui runge kutta
    return t, yeu



def runge_kutta_4(f, a, b, c0, h):
    n = int((b - a) / h)
    t = np.linspace(a, b, n + 1)
    yeu = [c0]
    for i in range(n):
        k1 = h * f(t[i], yeu[i])
        k2 = h * f(t[i] + 0.5 * h, yeu[i] + 0.5 * k1 )
        k3 = h * f(t[i] + 0.5 * h, yeu[i] + 0.5 * k2)
        k4 = h * f(t[i] + h, yeu[i] + k3 )
        yeu.append(yeu[i] + ((k1 + 2 * k2 + 2 * k3 + k4))/ 6)
    return t, yeu