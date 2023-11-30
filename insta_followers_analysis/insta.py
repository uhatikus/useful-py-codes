import json


def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def find_all_similar_usernames(username_list, threshold=4):
    similar_usernames_pairs = []

    for i, username1 in enumerate(username_list):
        for j, username2 in enumerate(username_list[i + 1 :]):
            distance = levenshtein_distance(username1, username2)
            if distance <= threshold:
                similar_usernames_pairs.append((username1, username2))

    return similar_usernames_pairs


def get_followers(filepath):
    # Read JSON data from file
    with open(filepath, "r") as file:
        json_data = file.read()

    # Parse JSON
    user_data = json.loads(json_data)

    # Create a set of usernames
    usernames_set = {user["username"] for user in user_data}
    return usernames_set


set1 = get_followers("followers_30_11_2023.json")
set2 = get_followers("followers_30_11_2023.json")

# Calculate the difference
unfollowed = set1 - set2
followed = set2 - set1


# Display the result
print(f"Unfollowed: {', '.join(unfollowed)}")
print()
print(f"New followers: {', '.join(followed)}")
print()

all_changed_usernames = list(unfollowed.union(followed))
similar_usernames_pairs = find_all_similar_usernames(all_changed_usernames)
print("Pairs of similar usernames:")
for pair in similar_usernames_pairs:
    print(f"{pair[0]} & {pair[1]}")
