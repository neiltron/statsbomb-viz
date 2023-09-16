# statsbomb dataviz
A few attempts displaying play-by-play type of data. These are experiments mostly to see what data is available for realtime dataviz and how to get said data. 

The current examples use [Statsbomb Open Data](https://github.com/statsbomb/open-data) but I want to find other, similar sources. The ultimate goal is use this data in Houdini/WebGL and/or build my own positional tracking system.

## Examples
There are currently two scripts here.

### 360 data
This data has freeze-frame events for a whole match. This includes `visible area` (what the camera sees), positional data for all players in view, as well as goalkeep/actor labels.

It doesn't have much else in terms of useful information. No player names, no timestamps, no play information, etc. I assume this is either available in the paid version or it needs to be inferred from separate event data. 

### Event data
This has detailed play-by-play information but is mostly limited to the involved players only; e.g., passer and receiver only. The exception is on shots on goal which contains a freeze frame of every player in the goal area.

Player coordinate data seems to be relative to the team and the example doesn't take this into account yet. Basically everything is left to right for both teams, so if possession changes, the player rendering appears to flip 180 degrees.


## Rendering
The scripts just output matplotlib pngs into directories and I'm using ffmpeg to compile into videos.

https://github.com/neiltron/statsbomb-viz/assets/452313/c85c7ed5-8c43-41b1-bae8-2cc80af3c848

https://github.com/neiltron/statsbomb-viz/assets/452313/fa12ad00-b324-4f2e-a32e-6d262726f39e
