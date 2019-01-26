import boto3
import time
import os
import logger


class AWSInstance(logger.Logger):
    """
    This class manage aws instances.
    """
    # Max retry.
    MAX_RETRY = 5
    # wait retry.
    WAIT_RETRY = 6

    def __init__(self, instance_id):
        super().__init__()

        # Check credentials
        if not os.environ['AWS_ACCESS_KEY_ID'] and os.environ['AWS_SECRET_ACCESS_KEY']:
            raise Exception("AWS credentials not found")

        # Connect with EC2.
        self.ec2 = boto3.resource(
            'ec2', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
            region_name='eu-west-1'
        )

        self.instance_id = instance_id
        self.retry = 0

    def get_public_ip(self, retry=0):
        """
        Verify machine state. If it is stopped, it is started.
        """
        # Start EC2 instance.
        for instance in self.ec2.instances.filter(InstanceIds=[self.instance_id]):
            # If instance is stopped, we start it.
            if instance.state['Name'] == 'stopped' and retry == 0:
                instance.start()

            # if instance is started, the we obtain public ip.
            if instance.state['Name'] == 'running':
                self.msg_info('Public IP: {}'.format(instance.public_ip_address))
                return instance.public_ip_address

            # wait to start.
            if retry < self.MAX_RETRY:
                self.msg_info('Waiting Instance Response.')
                time.sleep(self.WAIT_RETRY)
                return self.get_public_ip(retry + 1)
            # max retry number exceeded.
            self.msg_error('Public IP: Unknown. try again!!')
            return None

    def stop_instance(self, retry=0):
            # Start EC2 instance.
        for instance in self.ec2.instances.filter(InstanceIds=[self.instance_id]):
                # If instance is stopped, we start it.
                if instance.state['Name'] == 'running' and retry == 0:
                    instance.stop()
                    self.msg_info('Instance {} has been stopped'.format(self.instance_id))
                    return None
                else:
                    self.msg_info('Instance is already stopped')
                    return None

                # wait to start.
                if retry < self.MAX_RETRY:
                    self.msg_info('Waiting Instance Response.')
                    time.sleep(self.WAIT_RETRY)
                    return self.stop_instance(retry + 1)
                # max retry number exceeded.
                self.msg_error('Unexpected error, try again!!')
                return None


