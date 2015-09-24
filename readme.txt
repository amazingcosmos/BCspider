This is a little spider to gather user information on BlogCatalog.com.
It can get user's twitter homepage url and his following, followers, discussions.
The result will save as a txt named like username_following.txt.

[data structure]
user_detail_info:
<bc username>$||$<twitter url>$||$<followers(split by $**$)>$||$<following(split by $**$)>$||$<discussions(<title>$##$<href url>$##$<comment num>)(split by $**$)>