import getLMP
import getNodeMetadata
import processLMP
import csvToGeoJSON
import user_interface
import directory_setup as setup

if __name__ == "__main__":
    setup.create_folder('./data')

    iso_query = user_interface.getISO()
    getNodeMetadata.main(iso_query)

    starttime = user_interface.getStartTime()
    endtime = user_interface.getEndTime()
    getLMP.main(starttime,endtime)

    processLMP.main()
    csvToGeoJSON.main('NodeMetaData.csv')