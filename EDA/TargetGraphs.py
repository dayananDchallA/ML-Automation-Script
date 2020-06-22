import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
import os


class TargetGraphs:
    def __init__(self,df,colTypes,y,target_type,num_features=3):
        self.df = df.copy()
        self.y = y
        self.colTypes = colTypes
        self.num_features = num_features
        self.target_type = target_type
        self.target = self.df[y]
        self.corr_matrix = pd.Series()
        self.top_features = []
        self.plot_target_graphs()
    def plot_target_graphs(self):
        if self.y:
            corrMatrix = self.df.corr()
            fig = sns.heatmap(corrMatrix, annot=True, cmap='coolwarm', linewidth=2)
            figure = fig.get_figure()
            figure.savefig('C:\\Users\\RavikanthReddyKandad\Documents\\GitHub\\ML-Automation-Script-master\\static\\corr_pic.png',dpi=500)
            self.corr_matrix = self.df.corr().abs().unstack()
            self.corr_matrix = self.corr_matrix[self.y].sort_values(ascending=False)
            self.corr_matrix = self.corr_matrix.drop(self.y)
            self.corr_matrix = self.corr_matrix[0:self.num_features]
            self.top_features = self.corr_matrix.index.to_list()
            for feature in self.top_features:
                if feature in self.colTypes['Categorical'] and self.target_type in ['Categorical']:
                    fig = sns.catplot(x=self.y, y=feature,kind="swarm", data=self.df)
                    fig.savefig(
                        'C:\\Users\\RavikanthReddyKandad\Documents\\GitHub\\ML-Automation-Script-master\\static\\{}.png'.format(
                            feature))
                    fig = sns.catplot(x=self.y, y=feature,kind="violin", split=True,data=self.df)
                    fig.savefig(
                        'C:\\Users\\RavikanthReddyKandad\Documents\\GitHub\\ML-Automation-Script-master\\static\\1{}.png'.format(
                            feature))
                elif feature in (self.colTypes['Numeric'] or self.colTypes['Identity']) and self.target_type in ['Categorical']:
                    fig = sns.swarmplot(x=self.y, y=feature, data=self.df)
                    fig.figure.savefig('C:\\Users\\RavikanthReddyKandad\Documents\\GitHub\\ML-Automation-Script-master\\static\\{}.png'.format(feature))
                elif feature in self.colTypes['Categorical'] and self.target_type in ['Numeric', 'Identity']:
                    fig = sns.swarmplot(x=self.y, y=feature, data=self.df)
                    fig.figure.savefig(
                        'C:\\Users\\RavikanthReddyKandad\Documents\\GitHub\\ML-Automation-Script-master\\static\\{}.png'.format(
                            feature))
                elif feature in (self.colTypes['Numeric'] or self.colTypes['Identity']) and self.target_type in ['Numeric', 'Identity']:
                    fig = sns.relplot(x=self.y, y=feature, data=self.df)
                    fig.savefig(
                        'C:\\Users\\RavikanthReddyKandad\Documents\\GitHub\\ML-Automation-Script-master\\static\\{}.png'.format(
                            feature))

        if self.target_type in ['Categorical']:
            fig = sns.catplot(x=self.y, kind="count", palette="RdBu", data= self.df)
            fig.savefig('C:\\Users\\RavikanthReddyKandad\Documents\\GitHub\\ML-Automation-Script-master\\static\\target_categorical.png')
        elif self.target_type in ['Numeric','Identity']:
            mean = np.mean(self.target)
            median = self.target.median()
            mode = stats.mode(self.target)[0]
            if((mean == median) & (median == mode)):
                status = 'normal'
            else:
                sns.distplot(self.target).figure.savefig('C:\\Users\\RavikanthReddyKandad\Documents\\GitHub\\ML-Automation-Script-master\\static\\target_distribution.png')
                fig, ax = plt.subplots(1)
                ax = sns.distplot(self.target)
                fig.tight_layout()
                plt.savefig('C:\\Users\\RavikanthReddyKandad\Documents\\GitHub\\ML-Automation-Script-master\\static\\target_distribution.png')
                self.target = np.log10(self.target)
        #self.colTypes['Categorical'] = set(df.columns).intersection(set(colTypes['Categorical']))



