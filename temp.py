#%%
#sympy
import sympy
sympy.init_printing()

Y, X = sympy.symbols('Y, X')
Y = X**3 + 6*X**2 + 9
Y1 = Y.diff(X)
Y2 = Y.diff(X,X)

print(Y2)
# %%
