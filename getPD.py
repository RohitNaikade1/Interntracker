import pandas as pd


def get_gdp_data(modules,percentage):
    
    graph = {'Modules': modules,
                'Complete Percentage': percentage}
    data = pd.DataFrame(graph)
    return data