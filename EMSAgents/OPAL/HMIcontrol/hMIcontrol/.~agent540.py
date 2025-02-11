"""
Agent documentation goes here.
"""

__docformat__ = 'reStructuredText'

import logging
import sys
import json
from volttron.platform.agent import utils
from volttron.platform.vip.agent import Agent, Core, RPC

_log = logging.getLogger(__name__)
utils.setup_logging()
__version__ = "0.1"


def hMIcontrol(config_path, **kwargs):
    """
    Parses the Agent configuration and returns an instance of
    the agent created using that configuration.

    :param config_path: Path to a configuration file.
    :type config_path: str
    :returns: Hmicontrol
    :rtype: Hmicontrol
    """
    try:
        config = utils.load_config(config_path)
    except Exception:
        config = {}

    if not config:
        _log.info("Using Agent defaults for starting configuration.")

    setting1 = int(config.get('setting1', 1))
    setting2 = config.get('setting2', "some/random/topic")

    return Hmicontrol(setting1, setting2, **kwargs)


class Hmicontrol(Agent):
    """
    Document agent constructor here.
    """

    def __init__(self, setting1=1, setting2="some/random/topic", **kwargs):
        super(Hmicontrol, self).__init__(**kwargs)
        _log.debug("vip_identity: " + self.core.identity)

        self.setting1 = setting1
        self.setting2 = setting2

        self.default_config = {"setting1": setting1,
                               "setting2": setting2}

        # Set a default configuration to ensure that self.configure is called immediately to setup
        # the agent.
        self.vip.config.set_default("config", self.default_config)
        # Hook self.configure up to changes to the configuration file "config".
        self.vip.config.subscribe(self.configure, actions=["NEW", "UPDATE"], pattern="config")

    def configure(self, config_name, action, contents):
        """
        Called after the Agent has connected to the message bus. If a configuration exists at startup
        this will be called before onstart.

        Is called every time the configuration in the store changes.
        """
        config = self.default_config.copy()
        config.update(contents)

        _log.debug("Configuring Agent")

        try:
            setting1 = int(config["setting1"])
            setting2 = str(config["setting2"])
        except ValueError as e:
            _log.error("ERROR PROCESSING CONFIGURATION: {}".format(e))
            return

        self.setting1 = setting1
        self.setting2 = setting2

        self._create_subscriptions(self.setting2)

    def _create_subscriptions(self, topic):
        """
        Unsubscribe from all pub/sub topics and create a subscription to a topic in the configuration which triggers
        the _handle_publish callback
        """
        self.vip.pubsub.unsubscribe("pubsub", None, None)

        self.vip.pubsub.subscribe(peer='pubsub',
                                  prefix=topic,
                                  callback=self._handle_publish,all_platforms=True)

    def _handle_publish(self, peer, sender, bus, topic, headers, message):
        """
        Callback triggered by the subscription setup using the topic from the agent's config file
        """              
          
       
        print('999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999',message,topic)
        if topic=='Building540/HMIcontrol/battery/Drop_AC_Input':
            result=self.vip.rpc.call('platform.driver','set_point', 'building540/storage/Battery', topic.split('/')[-1],int(message))
        elif topic=='Building540/HMIcontrol/breakerb1/B1':
            result=self.vip.rpc.call('platform.driver','set_point', 'building540/breakers/ETON', topic.split('/')[-1],None)
            result=self.vip.rpc.call('platform.driver','set_point', 'building540/breakers/ETON', topic.split('/')[-1],int(message))
        elif topic=='Building540/HMIcontrol/breakerb1/B2':
            result=self.vip.rpc.call('platform.driver','set_point', 'building540/breakers/ETON', topic.split('/')[-1],None)
            result=self.vip.rpc.call('platform.driver','set_point', 'building540/breakers/ETON', topic.split('/')[-1],int(message))
        elif topic=='Building540/HMIcontrol/breakerb1/B3':
            result=self.vip.rpc.call('platform.driver','set_point', 'building540/breakers/ETON', topic.split('/')[-1],None)
            result=self.vip.rpc.call('platform.driver','set_point', 'building540/breakers/ETON', topic.split('/')[-1],int(message))
        elif topic=='Building540/HMIcontrol/breakerb1/B4':
            result=self.vip.rpc.call('platform.driver','set_point', 'building540/breakers/ETON', topic.split('/')[-1],None)
            result=self.vip.rpc.call('platform.driver','set_point', 'building540/breakers/ETON', topic.split('/')[-1],int(message))
        elif topic=='Building540/HMIcontrol/breakerb1/B5':
            result=self.vip.rpc.call('platform.driver','set_point', 'building540/breakers/ETON', topic.split('/')[-1],None)
            result=self.vip.rpc.call('platform.driver','set_point', 'building540/breakers/ETON', topic.split('/')[-1],int(message))
        elif topic=='Building540/HMIcontrol/breakerb1/B6':
            result=self.vip.rpc.call('platform.driver','set_point', 'building540/breakers/ETON', topic.split('/')[-1],None)
            result=self.vip.rpc.call('platform.driver','set_point', 'building540/breakers/ETON', topic.split('/')[-1],int(message))
        elif topic=='Building540/HMIcontrol/WeMo/all':
            self.vip.pubsub.publish('pubsub', "control/plc/NIRE_WeMo_cc_1/directcontrol", message=['all',int(message)])
#                result=agent.vip.rpc.call('platform.driver','set_point','building540/NIRE_WeMo_cc_1/w'+str(i),'priority',i)
             #Driectcontrol/all result=self.vip.rpc.call('platform.driver','set_point','building540/NIRE_WeMo_cc_1/w'+str(i),'status',int(message),external_platform='NIRE_WeMo_cc1').get(timeout=20)
        elif topic=='Building540/HMIcontrol/ClusterControl/Threshold/cc1':
            print('HAAAAAAAAAAAAAAAAAAAAAA')
#            Message= [{'Threashhold':int(message)},{'k':'Type'}]
            self.vip.pubsub.publish('pubsub', "control/plc/NIRE_WeMo_cc_1/PeakShaver", message=[{'Threashhold':int(message[0])},{'k':'Type'}])
           # print('BAAAAAAAAAAAAAAAAAAAAAAA')
        elif topic=='Building540/HMIcontrol/ClusterControl/Threshold/cc4':
            print('HAAAAAAAAAAAAAAAAAAAAAA')
#            Message= [{'Threashhold':int(message)},{'k':'Type'}]
            self.vip.pubsub.publish('pubsub', "control/plc/NIRE_WeMo_cc_4/PeakShaver", message=[{'Threashhold':int(message[0])},{'k':'Type'}])
         elif topic=='Building540/HMIcontrol/ClusterControl/Threshold/a1':
            print('HAAAAAAAAAAAAAAAAAAAAAA')
#            Message= [{'Threashhold':int(message)},{'k':'Type'}]
            self.vip.pubsub.publish('pubsub', "control/plc/NIRE_ALPHA_cc_2/PeakShaver", message=[{'Threashhold':int(message[0])},{'k':'Type'}])
         elif topic=='Building540/HMIcontrol/ClusterControl/Threshold/a2':
            print('HAAAAAAAAAAAAAAAAAAAAAA')
#            Message= [{'Threashhold':int(message)},{'k':'Type'}]
            self.vip.pubsub.publish('pubsub', "control/plc/NIRE_ALPHA_cc_1/PeakShaver", message=[{'Threashhold':int(message[0])},{'k':'Type'}])

        elif topic=='Building540/HMIcontrol/HVAC':
            if message['device']=='Ecobee1':
               result=agent.vip.rpc.call('platform.driver','set_point', 'Ecobee',message['operation'],message['data'])
        else:
            pass

          #  print('999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999',message,topic)


    @Core.receiver("onstart")
    def onstart(self, sender, **kwargs):
        """
        This is method is called once the Agent has successfully connected to the platform.
        This is a good place to setup subscriptions if they are not dynamic or
        do any other startup activities that require a connection to the message bus.
        Called after any configurations methods that are called at startup.

        Usually not needed if using the configuration store.
        """
        # Example publish to pubsub
        self.vip.pubsub.publish('pubsub', "some/random/topic", message="HI!")

        # Example RPC call
        # self.vip.rpc.call("some_agent", "some_method", arg1, arg2)
        pass

    @Core.receiver("onstop")
    def onstop(self, sender, **kwargs):
        """
        This method is called when the Agent is about to shutdown, but before it disconnects from
        the message bus.
        """
        pass

    @RPC.export
    def rpc_method(self, arg1, arg2, kwarg1=None, kwarg2=None):
        """
        RPC method

        May be called from another agent via self.core.rpc.call
        """
        return self.setting1 + arg1 - arg2


def main():
    """Main method called to start the agent."""
    utils.vip_main(hMIcontrol, 
                   version=__version__)


if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
