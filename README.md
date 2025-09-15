# mlb_wins_over_proj
Some simple code files that tracks my MLB Wins Over Projected Pool

Packages required: requests, pickle, datetime, pandas, dataframe_image

team_id_translate_no_names.py -> Takes data in from MLB API, team_info.txt, and draft_info.txt to make dictionaries needed to build report
** Output is id_to_customID_dict.pkl and id_to_draft_dict.pkl files

build_report -> This takes data in dictionaries and standings from MLB API and outputs report about who is currently ahead in MLB wins above projected pool
** Outputs total wins above projecteds, division leaders, and wild card teams each owner has
** Also outputs standings chart as an image
