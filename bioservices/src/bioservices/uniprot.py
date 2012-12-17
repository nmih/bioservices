"""



mappiung betwenn uniprot and bench of other DBs.

ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/idmapping/


"""
# Import SOAPpy WSDL package.
from SOAPpy import WSDL
from services import Service
import urllib2


class UniProt(Service):
    """


        >>> u = Uniprot()
        >>> data = u.fetchBatch("uniprot" ,"zap70_human", "xml", "raw")
        >>> import xml.etree.ElementTree as ET
        >>> root = ET.fromstring(data)


    URL can also be wsdlUrl = 'http://www.ebi.ac.uk/ws/services/WSDbfetch?wsdl'
    but it contains less methods

    """
    def __init__(self, name="UniProt",
            url='http://www.ebi.ac.uk/ws/services/WSDbfetchDoclit?wsdl',
            verbose=True, debug=False):
        super(UniProt, self).__init__(name=name, url=url, verbose=verbose)
        self._supportedDBs = None
        self._supportedFormats = None

    def _check_db(self, db):
        if db not in self.supportedDBs:
            raise Exception("%s not a supportedDB. " %db)


    def fetchBatch(self, db, ids, format="default", style="default"):
        """Fetch a set of entries in a defined format and style.

        :param str db: the name of the database to obtain the entries from (e.g., 'uniprotkb')
        :param list query: list of identifiers (e.g., 'wap_rat, wap_mouse')
        :param str format: the name of the format required. 
        :param str style: the name of the style required. 

        :returns: the format of the response depends on the interface to the service used:

            * WSDBFetchServerService and WSDBFetchDoclitServerService: the entries as a string.
            * WSDBFetchServerLegacyService: an array of strings containing the entries. 


        ::

            u = Uniprot()
            u.fetchBatch("uniprot" ,"wap_mouse", "xml")

        """
        return self.serv.fetchBatch(db, ids, format, style)

    def fetchData(self, query, format="default", style="default"):
        """Fetch an entry in a defined format and style.

        :param str query: the entry identifier in db:id format (e.g., 'UniProtKB:WAP_RAT')
        :param str format: the name of the format required. 
        :param str style: the name of the style required. 

        :returns: the format of the response depends on the interface to the service used:

            * WSDBFetchServerService and WSDBFetchDoclitServerService: the entries as a string.
            * WSDBFetchServerLegacyService: an array of strings containing the entries. Generally 
              this will contain only one item which contains the set of entries.

        ::

            u = Uniprot()
            u.fetchData('uniprot:zap70_human')

        """
        return self.serv.fetchData(query, format, style)


    def getDatabaseInfo(self, db):
        """Get details describing specific database (data formats, styles)

        .. note:: WSDBFetchDoclitServerService (document/literal) only.

        :param str db: a valid database 

        :: 

            u.getDatabseInfo("uniprotkb")

        .. seealso:: For details about the output, see http://www.ebi.ac.uk/Tools/webservices/services/dbfetch

        """
        self._check_db(db)
        return self.serv.getDatabaseInfo()

    def getDatabaseInfoList(self):
        """Get details of all available databases, includes formats and result styles.

        :Returns: a list of data structures describing the databases. See
            :meth:`getDatabaseInfo` for a description of the data structure.
        """

    def getDbFormats(self, db):
        """Get list of format names for a given database


        :param str db:

        """
        self._check_db(db)
        return self.serv.getDbFormats(db)
    

    def getFormatStyles(self, db, format):
        """Get a list of style names available for a given database and format.

        :param str db: database name to get available styles for (e.g., uniprotkb)
        :param str format: the data format to get available styles for (e.g., fasta)

        :Returns: an array of strings containing the style names. 

        ::

            >>> u.getFormatStyles("uniprotkb", "fasta")
            ['default', 'raw', 'html']
        """

        self._check_db(db)
        return self.serv.getFormatStyles(db, format)

    def getSupportedDBs(self):
        """Get a list of database names usable with WSDbfetch. 



        buffered in _supportedDB
        """
        if self._supportedDBs:
            return self._supportedDBs
        else:
            self._supportedDBs = self.serv.getSupportedDBs()
        return self._supportedDBs

    supportedDBs = property(getSupportedDBs)

    def getSupportedFormats(self):
        """Get a list of database and format names usable with WSDbfetch.

        .. deprecated:: use of getDbFormats(db), getDatabaseInfo(db) or  getDatabaseInfoList()



        """
        if self._supportedFormats == None:
            self._supportedFormats = self.serv.getSupportedFormats()
        return self._supportedFormats
    supportedFormats = property(getSupportedFormats)

    def getSupportedStyles(self):
        """Get a list of database and style names usable with WSDbfetch.

        .. deprecated:: use of getFormatStyles(db, format), getDatabaseInfo(db) or         getDatabaseInfoList() is recommended.

        Returns: an array of strings containing the database and style names. For example: 
        """
        retur.serv.getSupportedStyles()



    def mapping(self, fro="ID", to="KEGG_ID", format="tab", query="P13368"):
        """

        res = u.mapping(fro="ACC", to="KEGG_ID", query='P43403')
        res.split()
        ['From', 'To', 'P43403', 'hsa:7535']


        """
        import urllib
        url = 'http://www.uniprot.org/mapping/'
        params = {'from':fro, 'to':to, 'format':format, 'query':query}
        data = urllib.urlencode(params)
        print data
        request = urllib2.Request(url, data)
        contact = ""
        request.add_header('User-Agent', 'Python contact')
        response = urllib2.urlopen(request)
        result = response.read(200000)
        return result