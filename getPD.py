import pandas as pd


def get_gdp_data(modules, percentage, name, email,files):

    graph = {"Name": name,
             "emailId": email,
             'Induction Plan': modules,
             'Complete Percentage': percentage,
             'Sheet URL':files}
    data = pd.DataFrame(graph)
    return data
