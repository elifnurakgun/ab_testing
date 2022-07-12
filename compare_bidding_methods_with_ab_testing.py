#############################################
# AB Testi ile Bidding Yöntemlerinin Dönüşümünün Karşılaştırılması
#############################################

!pip install statsmodels
import numpy as np
import pandas as pd
import seaborn as sns
import itertools
import matplotlib.pyplot as plt
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# Görev 1:  Veriyi Hazırlama ve Analiz Etme

# ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz.
# Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.

df_control = pd.read_excel("/Users/Elifnur/Desktop/ab_testing.xlsx", sheet_name="Control Group")
df_test = pd.read_excel("/Users/Elifnur/Desktop/ab_testing.xlsx", sheet_name="Test Group")

# Kontrol ve test grubu verilerini analiz ediniz.
df_control.head()
df_test.head()

df_control.describe().T
df_test.describe().T

df_control.columns = [i+"_control" for i in df_control.columns]
df_test.columns = [i+"_test" for i in df_test.columns]

sms.DescrStatsW(df_control["Purchase_control"]).tconfint_mean()
sms.DescrStatsW(df_test["Purchase_test"]).tconfint_mean()

# Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.

df_mix = pd.concat([df_control, df_test], axis=1)
df_mix.head()

# Görev 2:  A/B Testinin Hipotezinin Tanımlanması

# Hipotezi tanımlayınız.

# H0: M1 = M2 (Average bidding ile maximum bidding'e ait purchase ortalamaları arasında istatistiksel olarak anlamlı bir fark yoktur.)
# H1: M1 != M2 (.... vardır.)

# Kontrol ve test grubu için purchase(kazanç) ortalamalarını analiz ediniz.

df_mix[["Purchase_control", "Purchase_test"]].mean()

# Görev 3:  Hipotez Testinin Gerçekleştirilmesi

# Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.
# Bunlar Normallik Varsayımı ve Varyans Homojenliğidir.
# Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni üzerinden ayrı ayrı test ediniz.

# Normallik Varsayımı:
# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1: Normal dağılım varsayımı sağlanmamaktadır.
# p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ!


test_stat, pvalue = shapiro(df_mix["Purchase_control"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# yorum: p-value = 0.5891 > 0.05 olduğundan dolayı, H0 reddedilemez.

test_stat, pvalue = shapiro(df_mix["Purchase_test"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# yorum: p-value = 0.1541 > 0.05 olduğundan dolayı, H0 reddedilemez.
# Normallik varsayımına göre normal dağılım varsayımı sağlanmaktadır. Yani H0 reddedilemez.


# Varyans Homojenliği:
# H0: Varyanslar homojendir.
# H1: Varyanslar homojen değildir.
# p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ!

test_stat, pvalue = levene(df_mix["Purchase_control"],
                           df_mix["Purchase_test"])
print("Test stat = %.4f, p-value = %.4f" % (test_stat, pvalue))

# yorum: p-value = 0.1083 > 0.05 olduğundan dolayı, H0 reddedilemez.
# Varyans Homojenliği varsayımı'na göre H0: Varyanslar homojendir varsayımı reddedilemez.


# Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz.

# Başvurulan: İki Örneklem T testi

test_stat, pvalue = ttest_ind(df_mix["Purchase_control"],
                              df_mix["Purchase_test"],
                              equal_var=True)
print("Test stat = %.4f, p-value = %.4f" % (test_stat, pvalue))

# yorum: p-value = 0.3493 > 0.05 olduğundan dolayı, H0 reddedilemez.

# Test sonucunda elde edilen p_value değerini göz önünde bulundurarak kontrol ve test grubu satın alma ortalamaları arasında istatistiki olarak anlamlı bir fark olup olmadığını yorumlayınız.

# Sonuç: Hipotez testlerinde belirtilen H0: reddedilemez.
# Maximum bidding ile average bidding'e ait purchase ortalamaları arasında istatistiksel olarak anlamlı bir fark yoktur.




