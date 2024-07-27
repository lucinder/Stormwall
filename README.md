Made this for a friend- based on their existing map layout, I set up a series of clustered vertices representing tunnel ends + randomized their connection (each tunnel end must connect to exactly 1 other tunnel end, tunnels that loop back to the same cavern are allowed).

Documentation in the code itself is low because this was thrown together in about 3 hours so here's the basics:

- Fill an array with numbers from 1 to 44 (the number of tunnel ends), randomize it, then have each index connect to the next index of the array for random connections
- Tunnels should take between 30 minutes to 1 week to traverse, with the ideal average traversal time being 8 hours (1 day travel), so heavily weighted in favor of lower times. To get this working:
  - Select a multiplier. Bigger multipliers means more left skew.
  - Multiply the max by this multiplier and get a "mean" to center the log function based on that.
  - Use numpy lognormal to randomize along the log distribution- sigma value determines spread. After some back and forth, we settled on 0.7.
  - Divide by the multiplier to force the values to the left.
   Currently, we're working with a multiplier of 3.5, which makes travel take in the 6-12 hour range normally.
- Build a networkx graph with the generated vertices, edges, and weights.
- All the prev is enough to build the txt file. Now to draw the graph:
  - Since the existing map is 50x50 grid of 70x70 tiles, use 50x50 mpl figure with 70dpi.
  - We want the tunnel edges to be centered around the same "caverns", but not overlapping. To do this:
      - Every tunnel edge maps to a cavern via a dict.
      - Every cavern has a set XY position, based on the original world map.
      - We grab the cavern XY and slap on a length-50px vector rotated based on the # of tunnel edges connecting to the cave.
  - Now for random color edges. Originally I had these tending dark, but I made them tending light after applying transparent background- random maps will be overlayed on an existing black background.
  - Label the edges with the weights and the vertices with the tunnel ids.
  - Export to png with transparency!
