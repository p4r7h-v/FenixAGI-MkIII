import numpy as np

def get_similar_users(user_ratings, target_user, num_recommendations=5):
    similarities = np.dot(user_ratings, target_user) / (np.linalg.norm(user_ratings, axis=1) * np.linalg.norm(target_user))
    most_similar_user_indices = np.argsort(similarities)[-num_recommendations:]
    return most_similar_user_indices

def get_recommendations(user_ratings, target_user_index, num_recommendations=5):
    target_user = user_ratings[target_user_index]

    # Get similar users
    similar_users = get_similar_users(user_ratings, target_user, num_recommendations)

    # Calculate the average ratings of similar users for items not rated by the target user
    items_not_rated = np.where(target_user == 0)[0]
    recommendations = np.mean(user_ratings[similar_users][:, items_not_rated], axis=0)

    # Get the indices of the top recommended items
    top_recommendations_indices = np.argsort(recommendations)[-num_recommendations:]
    return items_not_rated[top_recommendations_indices]

# Example usage
user_ratings = np.array([
    [5, 0, 3, 0, 1],
    [4, 0, 2, 5, 0],
    [0, 5, 1, 3, 0],
    [0, 5, 3, 3, 1],
    [0, 4, 0, 4, 0]
])

target_user_index = 0
num_recommendations = 2

recommended_items = get_recommendations(user_ratings, target_user_index, num_recommendations)
print("Recommended items for user {}:".format(target_user_index), recommended_items)