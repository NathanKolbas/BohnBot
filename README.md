# BohnBot

## About
The BohnBot was developed by Nathan Kolbas and is currently in use in our software engineering Discord server. It is mainly used for jokes and memes but can become much more. BohnBot is based off of [BradyBot](https://github.com/NathanKolbas/BradyBot). I guess you can say it has always been Brady.

## Features
The BohnBot's main feature is the ability to @ any user in the Discord which will then take their profile image and overlay it onto an Among Us gif. The overlaid image is also moving each frame. More features to be added in the future such as reading a random Bohn quote or adding a new one.

## Getting started
#### Installing
To install the required dependencies, simply run the command `pip install -r requirements.txt`. Optionally, for gif file size optimization to work please install [gifsicle](https://www.lcdf.org/gifsicle/). For example, gifscale reduces the file size of the Among Us gif generation by ~37%.

#### Setup
Create a `config.json` file in the root directory of the project. This will story secrets used by the bot.  Example `config.json` file:
```json
{
    "BOT_TOKEN": "bot_token",
    "GIS_DEV_API_KEY": "gis_api",
    "GIS_PROJECT_CX": "cx_project",
    "TWITTER_BEARER_TOKEN": "twitter_token"
}
```
The `BOT_TOKEN` is your Discord API key. Both `GIS_DEV_API_KEY` and `GIS_PROJECT_CX` are for Google image searching. Documentation for how to setup image search keys can be found [here](https://github.com/arrrlo/Google-Images-Search). `TWITTER_BEARER_TOKEN` is used by the Twitter API to get tweets. You will need to setup a Twitter developer account and create a new project found [here](https://developer.twitter.com/en/apply-for-access).

## Documentation
After adding the BohnBot to your Discord server, you can run the following commands:
  - `BohnBot execute @UserName`
    - Overlays the user profile icon, or image search, in an Among Us gif. The student being executed after one of Bohn's clever questions  
    ![example gif](Examples/example.gif)
  - `BohnBot kd|kills|executions|kill-count`
    - Tells you how many people Bohn has executed
  - `BohnBot smash|challenger @UserName`
    - Creates a gif of that user getting introduced in smash
    - Use the users @ in the command to use their icon in the gif
    - Type any text after to search for an image  
    ![example challenger_gif](Examples/example_challenger.gif)
  - `BohnBot quote`
    - Reads a random quote from the BohnDatabase
    - Optionally you can specify the line of the quote (e.g.`BohnBot quote 1`)
  - `BohnBot quote-all`
    - Shows all the quotes
  - `BohnBot add quote quote_text`
    - Add a quote to the BohnDatabase
  - `BohnBot remove-quote quote_line`
    - Removes a quote by the line. Requires Administrator permission to do so.
  - `BohnBot markov`
    - Creates a Markov chain using the quotes added to the BohnBot
  - `BohnBot stretch-break`
    - Starts a stretch break 
  - `BohnBot quine`
    - One of Bohn's favorite puzzles
  - `BohnBot tweet`
    - Gets a random tweet from DocBohn. (Limited to first 200 most recent tweets)
  - `BohnBot recent-tweet`
    - Gets the most recent tweet from DocBohn
  - `BohnBot new`
    - Tells you about what is new, features, improvements, and/or commands for the most recent update
  - `BohnBot help`
    - Help and commands for the BohnBot

## Contributing
Pull request are more than welcome. Feel free to contribute or fork the project for your own needs.
