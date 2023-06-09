#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# externals
import re
import pyre


# the app
class Viz(pyre.application):
    """
    Visualize the {ros3} access patterns
    """

    # the target file
    log = pyre.properties.istream()
    log.default = "s3.log"
    log.doc = "the logfile with the access info"

    svg = pyre.properties.ostream()
    svg.default = "s3.html"
    svg.doc = "the page with the visualization"

    scale = pyre.properties.float()
    scale.default = 0.5
    scale.doc = "the shrink factor"

    # interface
    @pyre.export
    def main(self, *args, **kwds):
        """
        The main entry point
        """
        # parse
        filesize, requests = self.parse()
        # generate the content
        content = "\n".join(self.generate(filesize=filesize, requests=requests))
        # and write it out
        print(content, file=self.svg)
        # all done
        return 0

    # implementation details - methods
    def parse(self):
        """
        Go through the log file and extract the access pattern data
        """
        # initialize the file size
        filesize = 0
        # and the accesses
        requests = []
        # get my parser
        parser = self.parser
        # read the file
        for line in self.log:
            # parse the line
            match = parser.match(line)
            # if it's not something we care about
            if match is None:
                # move on
                continue
            # extract
            size, request = match.groupdict().values()
            # if we got a size
            if size is not None:
                # record it
                filesize = int(size)
            # if we got a request
            if request is not None:
                # unpack and convert
                range = tuple(map(int, request.split()))
                # and store it
                requests.append(range)
        # all done
        return filesize, requests

    def generate(self, filesize, requests):
        """
        Write the page with the access pattern visualization
        """
        # compute the height of the graph
        height = 10 * len(requests)
        # first, the preamble
        yield self.preamble(height=height)
        # generate the plot
        yield from self.content(filesize=filesize, requests=requests, height=height)
        # finally, the epilogue
        yield self.epilogue()
        # all done
        return

    def content(self, filesize, requests, height):
        """
        Generate the top of the SVG output file
        """
        # get the scale
        scale = self.scale
        # set up the container
        yield f'        <g transform="translate(0 0) scale({scale} {scale})">'
        # go through the tick locations
        yield "          <!-- grid -->"
        for tick in range(1, 10):
            # draw the vertical lines
            yield f'          <path class="grid" d="M {100*tick} 0 l 0 {height}" />'
        # draw the box over the grid
        yield "          <!-- box -->"
        yield f'          <path class="axis" d="M 0 0 l 1000 0 l 0 {height} l -1000 0 Z" />'
        # go through the data requests
        yield "          <!-- requests -->"
        for index, (origin, size) in enumerate(requests):
            # compute the point coordinates
            x = 1000 * origin / filesize
            y = 10 * index + 4
            # scale the size
            width = 1000 * size / filesize
            # draw a line
            yield f'         <path class="access" d="M {x} {y} l {width} 0">'
            yield f"           <title>offset: {origin}, length: {size} bytes"
            yield f"         </path>"
        # close up
        yield "        </g>"
        # all done
        return

    def preamble(self, height):
        """
        Generate the page preamble
        """
        # get the scale
        scale = self.scale
        # generate
        return f"""
<!doctype html>

<!--
michael a.g. aïvázis <michael.aivazis@para-sim.com>
(c) 1998-2023 all rights reserved
-->

<html lang="en">

<head>
  <!-- meta -->
  <meta charset="utf-8" />
  <title>qed - ros3 data requests</title>


  <!-- default style sheet -->
  <link href="styles/qed.css" type="text/css" rel="stylesheet" media="all" />

  <!-- bookmark -->
  <link href="graphics/flame.png" type="image/png" rel="icon" />

  <!-- apple web app customizations -->
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-status-bar-style" content="black" />

</head>

<!-- body -->

<body>
  <div id="qed">
    <div id="graph">
      <svg id="canvas" version="1.1" xmlns="http://www.w3.org/2000/svg"
           height="{height*scale}px" width="{1000*scale}px">
"""

    def epilogue(self):
        """
        Generate the page epilogue
        """
        # easy
        return """
      </svg>
    </div>
  </div>

</body>
</html>

<!-- end of file -->
"""

    # implementation details -- data
    parser = re.compile(
        # starts with --
        r"\s--\s("
        # either size
        r"(size:\s(?P<size>\d+))"
        # or
        r"|"
        # byte range
        r"(request:\s(?P<request>\d+\s\d+))"
        # done
        r")"
    )


# bootstrap
if __name__ == "__main__":
    # instantiate
    app = Viz(name="s3.viz")
    # invoke
    status = app.run()
    # and share the status with the shell
    raise SystemExit(status)


# end of file
