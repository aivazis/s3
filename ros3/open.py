#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# externals
import pyre
import journal


# the app
class Open(pyre.application):
    """
    Trace {ros3} when opening/closing a file without any other activity
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
        channel = journal.info("s3.open")
        # make a timer
        timer = pyre.timers.wall("s3.open")
        # start it
        timer.start()
        # open the file
        pyre.h5.reader(uri=self.uri)
        # stop the timer
        timer.stop()
        # and show me
        channel.log(f"in {timer.sec()} sec")
        # and bail
        return 0


# bootstrap
if __name__ == "__main__":
    # instantiate
    app = Open(name="s3.open")
    # invoke
    status = app.run()
    # and share the status with the shell
    raise SystemExit(status)


# end of file
