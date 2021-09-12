import pandas as pd
import numpy as np
from scipy.stats import beta
from sklearn.model_selection import train_test_split
import config


class simulation:
    """ Functions for generating 1 dimensional simulation
    Parameters
    ----------
    rank: int, the number of simulation function
    """
    def __init__(self, rank) -> None:
        self.rank = rank

    def f_1(self, x):
        return np.sin(x) ** 2 + 0.1 + 0.6 * np.sin(2 * x) * np.random.randn(1)

    def f_2(self, x):
        return 2 * np.sin(x) ** 2 + 0.1 + 0.15 * x * np.random.randn(1)

    def f_3(self, x):
        x = np.random.poisson(np.sin(x) ** 2 + 0.1) + 0.08 * x * np.random.randn(1)
        x += 25 * (np.random.uniform(0, 1, 1) < 0.01) * np.random.randn(1)
        return x
    
    def f(self, x):
        x = np.random.poisson(np.sin(x) ** 2 + 0.1) + 0.03 * x * np.random.randn(1)
        x += 25 * (np.random.uniform(0, 1, 1) < 0.01) * np.random.randn(1)
        return x

    def generate(self, data):
        y = 0 * data
        for i in range(len(data)):
            if self.rank == 1:
                y[i] = self.f_1(data[i])
            elif self.rank == 2:
                y[i] = self.f_2(data[i])
            elif self.rank == 3:
                y[i] = self.f_3(data[i])
            else:
                y[i] = self.f(data[i])
        return y.astype(np.float32)


class GaussianDataGenerator(object):
    def __init__(self, px_model, mu_model, sigma_model):
        self.px_model = px_model
        self.mu_model = mu_model
        self.sigma_model = sigma_model
    
    def generate(self, size, **kwargs):
        if 'a' in kwargs:
            a = kwargs.pop('a')
            b = kwargs.pop('b')
            X = self.px_model(size, a=a, b=b)
        else:
            X = self.px_model(size)
        Y = self.mu_model(X) + self.sigma_model(X) * np.random.randn(size)
        return X, Y


def px_model(size, **kwargs):
    if 'a' in kwargs:
        a = kwargs.pop('a')
        b = kwargs.pop('b')
        return config.DataParams.left_interval + (config.DataParams.right_interval - config.DataParams.left_interval) * np.expand_dims(beta.rvs(a, b, size=size), 1)
    return config.DataParams.left_interval + (config.DataParams.right_interval - config.DataParams.left_interval) * np.random.rand(size, 1)


def mu_model(x):
    k = [1.0]
    b = -0.0
    return np.sum(k * x, axis=-1) + b 


def sigma_model(x):
    x_abs = np.abs(x)
    return (x_abs / (x_abs + 1)).reshape(-1)


def GetDataset(name, base_path, seed, test_ratio, a=1., b=1.):

    if 'simulation' in name:
        x_train = np.random.uniform(0, 5.0, size=config.DataParams.n_train).astype(np.float32)
        x_test = np.random.uniform(0, 5.0, size=config.DataParams.n_test).astype(np.float32)

        if '1' in name:
            sim = simulation(1)
        elif '2' in name:
            sim = simulation(2)
        elif '3' in name:
            sim = simulation(3)
        else:
            sim = simulation(4)

        y_train = sim.generate(x_train)
        y_test = sim.generate(x_test)
        x_train = np.reshape(x_train, (config.DataParams.n_train, 1))
        x_test = np.reshape(x_test, (config.DataParams.n_test, 1))
    
    if name == 'cov_shift':
        data_model = GaussianDataGenerator(px_model, mu_model, sigma_model)
        x_train, y_train = data_model.generate(config.DataParams.n_train)
        x_test, y_test = data_model.generate(config.DataParams.n_test, a=a, b=b)

    if name=="star":
        df = pd.read_csv(base_path + 'STAR.csv')
        df.loc[df['gender'] == 'female', 'gender'] = 0
        df.loc[df['gender'] == 'male', 'gender'] = 1
        
        df.loc[df['ethnicity'] == 'cauc', 'ethnicity'] = 0
        df.loc[df['ethnicity'] == 'afam', 'ethnicity'] = 1
        df.loc[df['ethnicity'] == 'asian', 'ethnicity'] = 2
        df.loc[df['ethnicity'] == 'hispanic', 'ethnicity'] = 3
        df.loc[df['ethnicity'] == 'amindian', 'ethnicity'] = 4
        df.loc[df['ethnicity'] == 'other', 'ethnicity'] = 5
        
        df.loc[df['stark'] == 'regular', 'stark'] = 0
        df.loc[df['stark'] == 'small', 'stark'] = 1
        df.loc[df['stark'] == 'regular+aide', 'stark'] = 2
        
        df.loc[df['star1'] == 'regular', 'star1'] = 0
        df.loc[df['star1'] == 'small', 'star1'] = 1
        df.loc[df['star1'] == 'regular+aide', 'star1'] = 2        
        
        df.loc[df['star2'] == 'regular', 'star2'] = 0
        df.loc[df['star2'] == 'small', 'star2'] = 1
        df.loc[df['star2'] == 'regular+aide', 'star2'] = 2   

        df.loc[df['star3'] == 'regular', 'star3'] = 0
        df.loc[df['star3'] == 'small', 'star3'] = 1
        df.loc[df['star3'] == 'regular+aide', 'star3'] = 2      
        
        df.loc[df['lunchk'] == 'free', 'lunchk'] = 0
        df.loc[df['lunchk'] == 'non-free', 'lunchk'] = 1
        
        df.loc[df['lunch1'] == 'free', 'lunch1'] = 0    
        df.loc[df['lunch1'] == 'non-free', 'lunch1'] = 1      
        
        df.loc[df['lunch2'] == 'free', 'lunch2'] = 0    
        df.loc[df['lunch2'] == 'non-free', 'lunch2'] = 1  
        
        df.loc[df['lunch3'] == 'free', 'lunch3'] = 0    
        df.loc[df['lunch3'] == 'non-free', 'lunch3'] = 1  
        
        df.loc[df['schoolk'] == 'inner-city', 'schoolk'] = 0
        df.loc[df['schoolk'] == 'suburban', 'schoolk'] = 1
        df.loc[df['schoolk'] == 'rural', 'schoolk'] = 2  
        df.loc[df['schoolk'] == 'urban', 'schoolk'] = 3

        df.loc[df['school1'] == 'inner-city', 'school1'] = 0
        df.loc[df['school1'] == 'suburban', 'school1'] = 1
        df.loc[df['school1'] == 'rural', 'school1'] = 2  
        df.loc[df['school1'] == 'urban', 'school1'] = 3      
        
        df.loc[df['school2'] == 'inner-city', 'school2'] = 0
        df.loc[df['school2'] == 'suburban', 'school2'] = 1
        df.loc[df['school2'] == 'rural', 'school2'] = 2  
        df.loc[df['school2'] == 'urban', 'school2'] = 3      
        
        df.loc[df['school3'] == 'inner-city', 'school3'] = 0
        df.loc[df['school3'] == 'suburban', 'school3'] = 1
        df.loc[df['school3'] == 'rural', 'school3'] = 2  
        df.loc[df['school3'] == 'urban', 'school3'] = 3  
        
        df.loc[df['degreek'] == 'bachelor', 'degreek'] = 0
        df.loc[df['degreek'] == 'master', 'degreek'] = 1
        df.loc[df['degreek'] == 'specialist', 'degreek'] = 2  
        df.loc[df['degreek'] == 'master+', 'degreek'] = 3 

        df.loc[df['degree1'] == 'bachelor', 'degree1'] = 0
        df.loc[df['degree1'] == 'master', 'degree1'] = 1
        df.loc[df['degree1'] == 'specialist', 'degree1'] = 2  
        df.loc[df['degree1'] == 'phd', 'degree1'] = 3              
        
        df.loc[df['degree2'] == 'bachelor', 'degree2'] = 0
        df.loc[df['degree2'] == 'master', 'degree2'] = 1
        df.loc[df['degree2'] == 'specialist', 'degree2'] = 2  
        df.loc[df['degree2'] == 'phd', 'degree2'] = 3
        
        df.loc[df['degree3'] == 'bachelor', 'degree3'] = 0
        df.loc[df['degree3'] == 'master', 'degree3'] = 1
        df.loc[df['degree3'] == 'specialist', 'degree3'] = 2  
        df.loc[df['degree3'] == 'phd', 'degree3'] = 3          
        
        df.loc[df['ladderk'] == 'level1', 'ladderk'] = 0
        df.loc[df['ladderk'] == 'level2', 'ladderk'] = 1
        df.loc[df['ladderk'] == 'level3', 'ladderk'] = 2  
        df.loc[df['ladderk'] == 'apprentice', 'ladderk'] = 3  
        df.loc[df['ladderk'] == 'probation', 'ladderk'] = 4
        df.loc[df['ladderk'] == 'pending', 'ladderk'] = 5
        df.loc[df['ladderk'] == 'notladder', 'ladderk'] = 6
        
        
        df.loc[df['ladder1'] == 'level1', 'ladder1'] = 0
        df.loc[df['ladder1'] == 'level2', 'ladder1'] = 1
        df.loc[df['ladder1'] == 'level3', 'ladder1'] = 2  
        df.loc[df['ladder1'] == 'apprentice', 'ladder1'] = 3  
        df.loc[df['ladder1'] == 'probation', 'ladder1'] = 4
        df.loc[df['ladder1'] == 'noladder', 'ladder1'] = 5
        df.loc[df['ladder1'] == 'notladder', 'ladder1'] = 6
        
        df.loc[df['ladder2'] == 'level1', 'ladder2'] = 0
        df.loc[df['ladder2'] == 'level2', 'ladder2'] = 1
        df.loc[df['ladder2'] == 'level3', 'ladder2'] = 2  
        df.loc[df['ladder2'] == 'apprentice', 'ladder2'] = 3  
        df.loc[df['ladder2'] == 'probation', 'ladder2'] = 4
        df.loc[df['ladder2'] == 'noladder', 'ladder2'] = 5
        df.loc[df['ladder2'] == 'notladder', 'ladder2'] = 6
        
        df.loc[df['ladder3'] == 'level1', 'ladder3'] = 0
        df.loc[df['ladder3'] == 'level2', 'ladder3'] = 1
        df.loc[df['ladder3'] == 'level3', 'ladder3'] = 2  
        df.loc[df['ladder3'] == 'apprentice', 'ladder3'] = 3  
        df.loc[df['ladder3'] == 'probation', 'ladder3'] = 4
        df.loc[df['ladder3'] == 'noladder', 'ladder3'] = 5
        df.loc[df['ladder3'] == 'notladder', 'ladder3'] = 6
        
        df.loc[df['tethnicityk'] == 'cauc', 'tethnicityk'] = 0
        df.loc[df['tethnicityk'] == 'afam', 'tethnicityk'] = 1
        
        df.loc[df['tethnicity1'] == 'cauc', 'tethnicity1'] = 0
        df.loc[df['tethnicity1'] == 'afam', 'tethnicity1'] = 1
        
        df.loc[df['tethnicity2'] == 'cauc', 'tethnicity2'] = 0
        df.loc[df['tethnicity2'] == 'afam', 'tethnicity2'] = 1
        
        df.loc[df['tethnicity3'] == 'cauc', 'tethnicity3'] = 0
        df.loc[df['tethnicity3'] == 'afam', 'tethnicity3'] = 1
        df.loc[df['tethnicity3'] == 'asian', 'tethnicity3'] = 2
        
        df = df.dropna()
        
        grade = df["readk"] + df["read1"] + df["read2"] + df["read3"]
        grade += df["mathk"] + df["math1"] + df["math2"] + df["math3"]
        
        
        names = df.columns
        target_names = names[8:16]
        data_names = np.concatenate((names[0:8],names[17:]))
        X = df.loc[:, data_names].values
        y = grade.values
        x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=test_ratio, random_state=seed)

    if name=="facebook_1":
        df = pd.read_csv(base_path + 'facebook/Features_Variant_1.csv')        
        y = df.iloc[:,53].values
        X = df.iloc[:,0:53].values        
    
    if name=="facebook_2":
        df = pd.read_csv(base_path + 'facebook/Features_Variant_2.csv')        
        y = df.iloc[:,53].values
        X = df.iloc[:,0:53].values 
        
    if name=="bio":
        #https://github.com/joefavergel/TertiaryPhysicochemicalProperties/blob/master/RMSD-ProteinTertiaryStructures.ipynb
        df = pd.read_csv(base_path + 'CASP.csv')        
        y = df.iloc[:,0].values
        X = df.iloc[:,1:].values        
        x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=test_ratio, random_state=seed)

    if name=='blog_data':
        # https://github.com/xinbinhuang/feature-selection_blogfeedback
        df = pd.read_csv(base_path + 'blogData_train.csv', header=None)
        X = df.iloc[:,0:280].values
        y = df.iloc[:,-1].values

    if name=="bike":
        # https://www.kaggle.com/rajmehra03/bike-sharing-demand-rmsle-0-3194
        df=pd.read_csv(base_path + 'bike_train.csv')
        
        # # seperating season as per values. this is bcoz this will enhance features.
        season=pd.get_dummies(df['season'],prefix='season')
        df=pd.concat([df,season],axis=1)
        
        # # # same for weather. this is bcoz this will enhance features.
        weather=pd.get_dummies(df['weather'],prefix='weather')
        df=pd.concat([df,weather],axis=1)
        
        # # # now can drop weather and season.
        df.drop(['season','weather'],inplace=True,axis=1)
        df.head()
        
        df["hour"] = [t.hour for t in pd.DatetimeIndex(df.datetime)]
        df["day"] = [t.dayofweek for t in pd.DatetimeIndex(df.datetime)]
        df["month"] = [t.month for t in pd.DatetimeIndex(df.datetime)]
        df['year'] = [t.year for t in pd.DatetimeIndex(df.datetime)]
        df['year'] = df['year'].map({2011:0, 2012:1})
 
        df.drop('datetime',axis=1,inplace=True)
        df.drop(['casual','registered'],axis=1,inplace=True)
        df.columns.to_series().groupby(df.dtypes).groups
        X = df.drop('count',axis=1).values
        y = df['count'].values
        x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=test_ratio, random_state=seed)

    if name == "concrete":
        dataset = np.loadtxt(open(base_path + 'Concrete_Data.csv', "rb"), delimiter=",", skiprows=1)
        X = dataset[:, :-1]
        y = dataset[:, -1:]
        x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=test_ratio, random_state=seed)

    if name == "community":
        # https://github.com/vbordalo/Communities-Crime/blob/master/Crime_v1.ipynb
        attrib = pd.read_csv(base_path + 'communities_attributes.csv', delim_whitespace = True)
        data = pd.read_csv(base_path + 'communities.data', names = attrib['attributes'])
        data = data.drop(columns=['state','county', 'community','communityname', 'fold'], axis=1)
        data = data.replace('?', np.nan)
        
        # Impute mean values for samples with missing values        
        from sklearn.impute import SimpleImputer
        
        imputer = SimpleImputer(missing_values = np.nan, strategy = 'mean')
        
        imputer = imputer.fit(data[['OtherPerCap']])
        data[['OtherPerCap']] = imputer.transform(data[['OtherPerCap']])
        data = data.dropna(axis=1)
        X = data.iloc[:, 0:100].values
        y = data.iloc[:, 100].values
        x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=test_ratio, random_state=seed)

    return x_train, x_test, y_train, y_test