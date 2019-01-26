#!/usr/bin/env python3

import sys
import os
import aws

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'ip':
        aws_instance = aws.AWS(os.environ['AWS_INSTANCE_ID'])
        ip = aws_instance.get_public_ip()
    elif len(sys.argv) > 1 and sys.argv[1] == 'help':
        print("""
        Options:
            ip -- get amazon EC2 ip
            help -- get command help
        """)
    else:
        print("Command not found")
