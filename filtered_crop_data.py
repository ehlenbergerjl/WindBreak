 # Filter out the outliers
ol_crop_data_iqr_rm = crop_data_orig[(crop_data_orig['indemnity'] >= lower_bound)
                                     & (crop_data_orig['indemnity'] <= upper_bound)][['yrmo', 'indemnity']]

# Filter out the outliers
ol_crop_data_std_rm = crop_data_orig[(crop_data_orig['indemnity'] >= lower_bound)
                                     & (crop_data_orig['indemnity'] <= upper_bound)][['yrmo', 'indemnity']]
