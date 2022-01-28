#import numpy as np
import pandas as pd


zips_dataframe = pd.read_csv('zips.csv')
plans_dataframe = pd.read_csv('plans.csv')
#join on rate area and state
merged_frame = zips_dataframe.merge(plans_dataframe, how='inner', left_on=['rate_area', 'state'], right_on=['rate_area', 'state'])
#filter out noise, ie just the silver
chromed_out_frame = merged_frame.loc[merged_frame['metal_level']=='Silver']
#get two smallest plans by rate area and zipcode
distilled = chromed_out_frame.groupby(['zipcode', 'rate_area'])['rate'].nsmallest(2).groupby(['zipcode', 'rate_area']).last()
distilled.to_csv('deDuped.csv')
further_distilled = distilled.reset_index()


slcsp = pd.read_csv('slcsp.csv')

final_merge = slcsp.merge(further_distilled, how='left', left_on=['zipcode'], right_on=['zipcode'])


filtered_final_result = final_merge[["zipcode", "rate_y"]]
filtered_final_result = filtered_final_result.rename(columns={"rate_y": "rate"})

filtered_final_result.to_csv('slcsp.csv', index=False, float_format='%.2f')

