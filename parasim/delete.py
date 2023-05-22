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

# delete
s3.delete_object(Bucket=bucket, Key=name)

# show me
print(f"deleted '{bucket}/{name}'")


# end of file
