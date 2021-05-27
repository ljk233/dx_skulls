# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:hydrogen
#     text_representation:
#       extension: .py
#       format_name: hydrogen
#       format_version: '1.3'
#       jupytext_version: 1.11.1
#   kernelspec:
#     display_name: Python 3.8
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Comparing skull sizes of Etruscans and modern Italian men

# %% [markdown]
# ## Aim
#
# Perform an hypothesis comparing the mean skull breadth of the ancient Etruscan
# people of Italy with that of modern native Italians.

# %% [markdown]
# ## Setup

# %%
# import packages and modules
from scipy.stats import probplot, t, ttest_ind
from math import sqrt
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# %% [code]
# sets Seaborn theme
sns.set_theme()

# %% [markdown]
# ## Load

# %%
skulls = pd.read_csv("..\\data\\skulls.csv")

# %% [markdown]
# ## Explore

# %% [markdown]
# ### Preview

# %%
skulls.head()

# %% [markdown]
# ### Describe

# %%
skulls.describe().T

# %% [markdown]
# ### Plot

# %%
# unpivots the data (wide -> long)
mskulls = skulls.melt(
    value_vars=["Etruscans", "Italians"],
    var_name="skull",
    value_name="size")

mskulls.dropna(inplace=True)
mskulls["size"] = mskulls["size"].astype("int")  # receast the data

# %%
g = sns.FacetGrid(mskulls, col="skull")
g.map_dataframe(sns.histplot, x="size", bins=10)
plt.show()

# %%
sns.boxplot(data=mskulls, x="size", y="skull")
plt.show()

# %% [markdown]
# ## Analyse

# %% [markdown]
# ### Probability plots

# %%
f, (ax1, ax2) = plt.subplots(ncols=2, sharey=True)

probplot(x=skulls["Etruscans"], plot=ax1)
ax1.set(title="Probability plot = Etruscans")

probplot(x=skulls["Italians"].dropna(), plot=ax2)
ax2.set(title="Probability plot = Italians")

plt.show()

# %% [markdown]
# ### Test common variance

# %% [code]
skulls["Etruscans"].var() > skulls["Italians"].var()

# %% [markdown]
# ### Get 95% $t$-intervals

# %%
etr = skulls["Etruscans"]
t_etr = t(df=etr.size - 1, loc=etr.mean(), scale=etr.std() / sqrt(etr.size))
t_etr.interval(0.95)

# %%
ita = skulls["Italians"]
t_ita = t(df=ita.size - 1, loc=ita.mean(), scale=ita.std() / sqrt(ita.size))
t_ita.interval(0.95)

# %% [markdown]
# ### Perform hypothesis test

# %%
ttest_ind(a=etr, b=ita, nan_policy="omit", alternative="two-sided")
