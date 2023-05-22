#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved

import boto3

# set the path to the file
bucket = "parasim-qed"
name = "strm.tif"

# start a session
s3 = boto3.Session(profile_name="parasim").client("s3")

# get the file
with open(f"{bucket}/{name}", mode="rb") as stream:
    # upload
    s3.upload_fileobj(stream, bucket, name)

# show me
print(f"uploaded '{bucket}/{name}'")


# end of file
