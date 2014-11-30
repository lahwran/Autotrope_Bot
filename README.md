Autotrope_Bot
=============
This bot finds links on reddit that lead to TvTropes.org, and posts a summary of them.

## Creating your own instance
### Dependencies
* Beautiful Soup
* PRAW

### Editing the datafile
1. Rename `data_file_example.inf` to `data_file.inf`.
2. Replace `bot_name` with the account's name.
3. Replace `bot_password` with the account's password.
4. Replace `all` with the subreddit you want to scrape  
  *Don't leave it as `all` - conflicts will occur with the official bot.*
5. Leave the next 2 lines as-is.
6. The last line is the minimum character length, used to stop 1-liners. 600 is a good value.

### Launching the program
To launch the prgram, run `python autotrope_bot.py`  
To run the deleter, on a seperate console run `python remove_negative.py`  
To quit the program, use `ctrl + c`
