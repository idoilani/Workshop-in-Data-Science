import pandas as pd
import numpy as np


def create_user_total_scores_by_clusters(df):
    u_id = 'OwnerUserId_ans'
    all_clstrs = filter(lambda field: str(field).startswith('cluster_'), list(df))

    amount_tags_per_q = pd.Series(np.zeros(len(df[u_id])))
    for cluster in all_clstrs:
        amount_tags_per_q = amount_tags_per_q.add(df[cluster], fill_value=0)
    for_inner_multi = [df[cluster] * df['user_score_' + cluster] for cluster in all_clstrs]
    s = pd.Series(np.zeros(len(for_inner_multi[0])))
    for i in range(len(for_inner_multi)):
        s = s.add(for_inner_multi[i], fill_value=0)
    df['total_score_user_question_by_clusters'] = s.astype(float)
    df['total_score_user_question_by_clusters_relative'] = (s.astype(float) / amount_tags_per_q.astype(float)).fillna(0)

    return df


def users_scores_clusters(df):
    # WARNING: this function consider the result of isAcceptedAnswer
    # ONLY USE ON TRAIN

    u_id = 'OwnerUserId_ans'
    is_acc = 'IsAcceptedAnswer'
    all_clstrs = filter(lambda field: str(field).startswith('cluster_'), list(df))

    # score by clusters:
    for cluster in all_clstrs:
        D = {}
        for user, gr in df.groupby(u_id):
            D[user] = (gr[cluster].sum(), (gr[cluster]*gr[is_acc]).sum())
        tmp_series = df[u_id].apply(lambda x: (0 if D[x][0] == 0 else D[x][1] / float(D[x][0])))
        df['user_score_' + cluster] = tmp_series.astype(float)

    # general_score = user_amount_true / user_amount_questions
    D = {}
    for user, gr in df.groupby(u_id):
        D[user] = (len(gr), np.count_nonzero(gr[is_acc]))

    tmp_series = df[u_id].apply(lambda x: (0 if D[x][0] == 0 else D[x][1] / float(D[x][0])))
    df['user_score_general'] = tmp_series.astype(float)

    return df
