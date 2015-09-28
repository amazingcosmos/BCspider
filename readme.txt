This is a little spider to gather user information on BlogCatalog.com. It can get user's twitter homepage url and his following, followers, discussions. The result will save as a txt named like username.txt.

[user_info data structure]
user_detail_info:
<bc username>$||$<twitter url>$||$<followers_num>$||$<following_num>$||$<blog_num>$||$<reading_num>$||$<discussion_num>
<followers(split by $||$)>
<following(split by $||$)>
<discussions_title>$||$<href url>$||$<comment num>
<discussions_title>$||$<href url>$||$<comment num>
<discussions_title>$||$<href url>$||$<comment num>
...

The best way to use this module on windows is to click the run.bat. But before you do it, make sure you have
put a user_todo.txt, contains the username of blogcatalog you want to get info from at each line, to the ./filter folder(Each username each line :)