# weather
Console weather parser (sinoptik.ua).

First steps:
1) Clone my repository if you didn't that. 'git clone https://github.com/lopolen/weather/';
2) In first time run 'pip install -r requirements.txt' from project directory;
3) Then you can replace weather.py to place what you need;

Usage:
  python weather.py [PARAMETERS]
  -t --today                Shows weather forecast for today. Default;
  -w --week                 Shows weather forecast for this week. Excludes the '-t' parameter;
  -c --city [CITY_NAME]     Set city. Default parse main page of sinoptik.ua.
  
I hope you enjoed. 'sinoptik.ua' is Ukrainian site and there may be inaccuracies with forecasts outside of Ukraine.
You can contact me using mail 'li6665864@gmail.com'.
