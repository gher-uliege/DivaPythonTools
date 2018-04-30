__author__ = 'ctroupin'
'''User interface for diva in python'''

import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


class DivaUser(object):
    '''The DivaUser represents the user that will run the code remotely
    on the EUDAT infrastructure. Depending on the project developments,
    the information on the user can be variable.
    '''

    def __init__(self, name, affiliation, project, SDNregion, orcid):
        """

        :type name: string:
        :type orcid: string
        """
        self.name = name
        self.affiliation = affiliation
        self.project = project
        self.SDNregion = SDNregion

        self.orcid = orcid

    def give_user_details(self):
        print("User name: {0}".format(self.name))
        print("Affiliation: {0}".format(self.affiliation))
        print("Project: {0}".format(self.project))
        if self.project.lower() == 'seadatacloud':
            print("SDN region: {0}".format(self.SDNregion))
        if self.orcid:  # Check if the orcID is defined
            print("OrcID number: {0}".format(self.orcid))


logger.debug("Create new Diva user")
user0001 = DivaUser('Charles Troupin', 'GHER-ULg', 'SeaDataCloud', '', '0000-0002-0265-1021')
user0001.give_user_details()
