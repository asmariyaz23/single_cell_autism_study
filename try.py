import rpy2.robjects as robjects
from rpy2.robjects import r
from rpy2.robjects.numpy2ri import numpy2ri
from rpy2.robjects.packages import importr
import numpy as np

cont = np.reshape(np.arange(0,4), (2,2))
print(cont)

r_cont = numpy2ri(cont)
r.assign("cont", r_cont)
r("res <- fisher.test(cont, simulate.p.value = TRUE, B = 100)")
r_result = r("res")
p_value = r_result[0][0]
print(r_result)
print(p_value)
