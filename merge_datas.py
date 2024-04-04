import pandas as pd



def main():
    df_parking = pd.read_csv('./parking_by_place.csv')
    df_cctv = pd.read_csv('./cctv_feature_1208.csv', index_col=0)
    df_light_train = pd.read_csv("./train_light.csv")
    df_light_test = pd.read_csv("./test_light.csv")

    df_ice = pd.read_csv('./df_ice.csv', index_col=0).drop(columns='id')
    df_old = pd.read_csv('./df_old.csv', index_col=0).drop(columns='id')
    df_pds = pd.read_csv('./df_pds.csv', index_col=0).drop(columns='id')
    df_trk = pd.read_csv('./df_trk.csv', index_col=0).drop(columns='id')
    df_wlk = pd.read_csv('./df_wlk.csv', index_col=0).drop(columns='id')

    df_merged_train = pd.merge(df_light_train, df_parking, on='시군구', how='left')
    df_merged_test = pd.merge(df_light_test, df_parking, on='시군구', how='left')

    df_merged_train = pd.merge(left=df_merged_train, right=df_cctv, on='시군구', how='left')
    df_merged_test = pd.merge(left=df_merged_test, right=df_cctv, on='시군구', how='left')

    loc_taxi_info = pd.read_csv('./data_child_taxi.csv', index_col=0)[['시군구','보호구역도로폭_카테고리', '어린이보호구역 개수', '어보구CCTV설치비율', '하차', '승차']]

    lti_group = loc_taxi_info.groupby('시군구').mean()

    df_merged_train = pd.merge(left=df_merged_train, right=lti_group, on='시군구', how='left')
    df_merged_test = pd.merge(left=df_merged_test, right=lti_group, on='시군구', how='left')

    df_total_danger = pd.concat([df_ice['시군구'], (df_ice.iloc[:,1:] + df_old.iloc[:,1:] + df_pds.iloc[:,1:] + df_trk.iloc[:,1:] + df_wlk.iloc[:,1:])],axis=1)

    df_total_danger = df_total_danger[['시군구','count'] + [col for col in df_old.columns if 'sum' in col or 'total' in col]]

    df_merged_train = pd.merge(left=df_merged_train, right=df_total_danger, on='시군구', how='left')
    df_merged_test = pd.merge(left=df_merged_test, right=df_total_danger, on='시군구', how='left')

    return df_merged_train, df_merged_test

if __name__ == '__main__':
    df_merged_train, df_merged_test = main()

    df_merged_train.to_csv('./final_train.csv', index=False)
    df_merged_test.to_csv('./final_train.csv', index=False)