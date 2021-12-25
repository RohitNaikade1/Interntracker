import pandas as pd


def get_gdp_data(modules, percentage, name, email):

    graph = {"Name": name,
             "emailId": email,
             'Induction Plan': modules,
             'Complete Percentage': percentage}
    data = pd.DataFrame(graph)
    return data
