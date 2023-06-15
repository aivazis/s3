#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# externals
import pyre
import journal


# the app
class Read(pyre.application):
    """
    Trace {ros3} when discovering the structure of an empty NISAR rslc data product
    """

    # the target file
    uri = pyre.properties.uri()
    uri.default = "s3://parasim@eu-central-1/fsm-64k/rslc.h5"
    uri.doc = "the target file URI"

    # interface
    @pyre.export
    def main(self, *args, **kwds):
        """
        The main entry point
        """
        # make a channel
        channel = journal.info("s3.read")
        # make a timer
        timer = pyre.timers.wall("s3.read")
        # start it
        timer.start()
        # read the file
        pyre.h5.read(uri=self.uri)
        # stop the timer
        timer.stop()
        # and show me
        channel.log(f"in {timer.sec()} sec")
        # and bail
        return 0


# bootstrap
if __name__ == "__main__":
    # instantiate
    app = Read(name="s3.read")
    # invoke
    status = app.run()
    # and share the status with the shell
    raise SystemExit(status)


# end of file
