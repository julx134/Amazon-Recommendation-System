from collections import defaultdict
from surprise.model_selection import cross_validate
from surprise import KNNBasic
from surprise import Dataset, SVD


def get_top_n(predictions, n=10):
    """Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n(int): The number of recommendation to output for each user. Default
            is 10.

    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    """

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n


# First train the algorithm on the movielens dataset.
data = Dataset.load_builtin("ml-100k")
trainset = data.build_full_trainset() ##returns dataset as a trainset object with no folds

# set-up options for RS algorithm
sim_options = {
    "name": "cosine",
    "user_based": False,  # compute  similarities between items
}
#initialize RS algorithm to be IBCF
algo = KNNBasic(sim_options=sim_options)

#train IBCF on the trainset
#algo.fit(trainset)

# Than predict ratings for all pairs (u, i) that are NOT in the training set.
#testset = trainset.build_anti_testset()
#predictions = algo.test(testset)

# Run 5-fold cross-validation and print results
cross_validate(algo, data, measures=["RMSE", "MAE"], cv=5, verbose=True)

#top_n = get_top_n(predictions, n=10)

# Print the recommended items for each user
#for uid, user_ratings in top_n.items():
    #print(uid, [iid for (iid, _) in user_ratings])
