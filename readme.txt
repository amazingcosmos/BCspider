This is a little spider to gather user information on BlogCatalog.com.
It can get user's twitter homepage url and his following, followers, discussions.
The result will save as a txt named like username_following.txt.

[user_info data structure]
user_detail_info:
<bc username>$||$<twitter url>$||$<followers_num>$||$<following_num>$||$<blog_num>$||$<reading_num>$||$<discussion_num>
<followers(split by $||$)>
<following(split by $||$)>
<discussions_title>$||$<href url>$||$<comment num>