#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved

# aws support
import boto3

# set the path to the file
bucket = "parasim-ros3eu"
name = "README.txt"

# start a session
s3 = boto3.Session(profile_name="parasim").client("s3")

# download
s3.download_file(bucket, name, f"{bucket}/{name}")

# show me
print(f"downloaded '{name}'")


# end of file
