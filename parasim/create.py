#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved

# aws support
import boto3

# build the path to the file
region = "eu-central-1"
bucket = "parasim-qed"

# start a session
s3 = boto3.Session(profile_name="parasim").client("s3")

# create a bucket
s3.create_bucket(
    Bucket=bucket,
    CreateBucketConfiguration={"LocationConstraint": region},
)
# show me
print(f"created '{bucket}'")


# end of file
