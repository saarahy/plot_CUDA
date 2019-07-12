import pandas as pd
import matplotlib.pyplot as plt
import plotnine as p9
import random as rd

#  Cargas el archivo donde tienes la lista con los nombres de los archivos generados
#  en CUDA. Recuerda que debe de tener un header con la etiqueta de: name_file

df= pd.read_csv("./script_GP1_.csv")

df_new_1 = pd.DataFrame(columns=[ 'run', 'popsize', 'indsize',
                        'nrow', 'nvar', 'timewr', 'timewo', 'diff']);
df_new_2 = pd.DataFrame(columns=[ 'run', 'popsize', 'indsize',
                        'nrow', 'nvar', 'timewr', 'timewo', 'diff']);
df_new_3 = pd.DataFrame(columns=['run', 'popsize', 'indsize',
                        'nrow', 'nvar', 'timewr', 'timewo', 'diff']);
df_new_4 = pd.DataFrame(columns=[ 'run', 'popsize', 'indsize',
                        'nrow', 'nvar', 'timewr', 'timewo', 'diff']);

df_gb = pd.DataFrame(columns=[ 'run', 'popsize', 'indsize',
                        'nrow', 'nvar', 'timewr', 'timewo', 'diff']);
df_test = pd.DataFrame(columns=['time']);

for index, row in df.iterrows():
    try:
        #  Aqui pones la direccion donde se encuentran todos los archivos generados en CUDA.
        df_n = pd.read_csv("./script_GP1/%s" % row['name_file'], delimiter=',', header = None)

        df_n.columns = ['run', 'popsize', 'indsize',
                        'nrow', 'nvar', 'timewr', 'timewo', 'diff']
        if(df_n['popsize'][0]==1024):
            df_new_1 = df_new_1.append(df_n, ignore_index=True)
        elif(df_n['popsize'][0]==10240):
            df_new_2 = df_new_2.append(df_n, ignore_index=True)
        elif (df_n['popsize'][0] == 102400):
            df_new_3 = df_new_3.append(df_n, ignore_index=True)
            # += 1
        elif (df_n['popsize'][0] == 1048576):
            df_new_4 = df_new_4.append(df_n, ignore_index=True)
    except:
        continue

df_1 = df_new_1.groupby(['nrow' , 'nvar'])['timewr'].mean()
df_1.to_csv('/home/treelab/Documents/CUDAGP/script_GP1/graphs/mean_%s_%s.csv'%(df_new_1['popsize'][0], df_new_1['indsize'][0]))
df_2 = df_new_2.groupby(['nrow' , 'nvar'])['timewr'].mean()
df_2.to_csv('/home/treelab/Documents/CUDAGP/script_GP1/graphs/mean_%s_%s.csv'%(df_new_2['popsize'][0], df_new_2['indsize'][0]))
df_3 = df_new_3.groupby(['nrow' , 'nvar'])['timewr'].mean()
df_3.to_csv('/home/treelab/Documents/CUDAGP/script_GP1/graphs/mean_%s_%s.csv'%(df_new_3['popsize'][0], df_new_3['indsize'][0]))
try:
    df_4 = df_new_4.groupby(['nrow' , 'nvar'])['timewr'].mean()
    df_4.to_csv('/home/treelab/Documents/CUDAGP/script_GP1/graphs/mean_%s_%s.csv'%(df_new_4['popsize'][0], df_new_4['indsize'][0]))
except:
    print 'error'

for ielem in (df_new_1, df_new_2, df_new_3, df_new_4):
    surveys_plot =(p9.ggplot(data=ielem,
               mapping=p9.aes(x='run',
                              y='timewr',
                              color='factor(nvar)'))
                   + p9.geom_point()
                   + p9.facet_grid("~nrow")
                   + p9.scale_y_continuous(limits=(0,500))
                   + p9.scale_x_discrete(breaks=range(0,35,5))
                   +p9.theme(text=p9.element_text(size=10, family="serif"),
                              plot_title=p9.element_text(weight='bold', size=14),
                              legend_title=p9.element_text(weight='bold', size=14),
                              legend_text=p9.element_text(weight='bold', size=10),
                              axis_title_y =p9.element_text(weight='bold', size=14),
                              axis_title_x =p9.element_text(weight='bold', size=14)
                              )
                   + p9.labs(y='Time (s)', x='Number of run', title='Population Size [%s]'%ielem['popsize'][0], color='Features')
    )
    #  Cambiar a la direccion donde quieres guardarlos
    surveys_plot.save("./data_%s_%s.pdf"%(ielem['popsize'][0], ielem['indsize'][0]),width=11, height=8.5, dpi=300)

