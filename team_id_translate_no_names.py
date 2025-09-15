import requests
import pickle

# Call the MLB StatsAPI endpoint to get MLB teams & ID data
url = "https://statsapi.mlb.com/api/v1/teams?sportId=1"
response = requests.get(url)
data = response.json()

# Build api_team_to_id_dict dictionary {team_name: team_id}
api_team_to_id_dict = {team['name']: team['id'] for team in data['teams']}

# # Print out the dictionary
# print("Team dictionary (name -> id):")
# for name, tid in api_team_to_id_dict.items():
#     print(f"{name}: {tid}")

# Get Team Name and Custom ID from text file (team_info.txt)
with open("team_info.txt", "r") as ff:
    lines = ff.readlines()

# Create custom_team_to_id_dict with info from text file (team_info.txt)
custom_team_to_id_dict = {}
for line in lines:
    split_line = line.split(", ")
    custom_team_to_id_dict[split_line[1]] = [split_line[0], split_line[2][:-1]]

# # Print out the dictionary
# print("Team dictionary (name -> id, divison):")
# for name, data in custom_team_to_id_dict.items():
#     print(f"{name}: {data}")
# print(len(custom_team_to_id_dict))

#Create id_to_customId_dict to go between MLB Stats API ID and Custom ID
id_to_customId_dict = {}
for key in api_team_to_id_dict.keys():
    id_to_customId_dict[api_team_to_id_dict[key]] = custom_team_to_id_dict[key]

# # Print out the dictionary
# print("Team dictionary (id -> customId, divison):")
# for id, data in id_to_customId_dict.items():
#     print(f"{id}: {data}")
# print(len(id_to_customId_dict))

# Save to id_to_customID_dict as pickle file
with open("id_to_customID_dict.pkl", "wb") as ff:
    pickle.dump(id_to_customId_dict, ff)
print("Dictionary saved to id_to_customID_dict.pkl")

# Get Draft Info from text file (draft_info.txt)
with open("draft_info.txt", "r") as ff:
    lines = ff.readlines()


# Create id_to_draft_dict with info from text file (draft_info.txt)
id_to_draft_dict = {}
for line in lines:
    split_line = line.split(", ")
    id_to_draft_dict[split_line[0]] = [float(split_line[1]), int(split_line[2])]

# # Print out the dictionary
# print("Team dictionary (id -> wins_proj, owner):")
# for id, data in id_to_draft_dict.items():
#     print(f"{id}: {data}")
# print(len(id_to_draft_dict))

# Save to id_to_draft_dict as pickle file
with open("id_to_draft_dict.pkl", "wb") as ff:
    pickle.dump(id_to_draft_dict, ff)
print("Dictionary saved to id_to_draft_dict.pkl")



